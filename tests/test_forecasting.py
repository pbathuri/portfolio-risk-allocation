from pathlib import Path
import json
import io
from contextlib import redirect_stdout
import sys
import tempfile
import subprocess
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from forecasting import checkpoint, engineer, synthetic, validate, split_dates, weighted_metrics
from prepare_forecasting import prepare
from inspect_source import inspect


class ForecastingTests(unittest.TestCase):
    def test_weighted_metric_hand_calculation(self):
        result = weighted_metrics([1, 2], [0, 1], [1, 3])
        self.assertAlmostEqual(result['weighted_rmse'], 1)
        self.assertAlmostEqual(result['weighted_zero_mean_r2'], 1 - 4/13)

    def test_zero_denominator_is_undefined(self):
        self.assertIsNone(weighted_metrics([0], [1], [1])['weighted_zero_mean_r2'])

    def test_invalid_weights_rejected(self):
        for weights in ([0, 0], [-1, 2], [np.nan, 1]):
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                weighted_metrics([1, 2], [1, 2], weights)

    def test_duplicate_keys_rejected(self):
        data = synthetic()
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate(pd.concat([data, data.iloc[:1]]))

    def test_whole_dates_are_strictly_separated(self):
        data = validate(synthetic())
        masks = split_dates(data)
        self.assertLess(data.loc[masks['train'], 'date_id'].max(), data.loc[masks['validation'], 'date_id'].min())
        self.assertLess(data.loc[masks['validation'], 'date_id'].max(), data.loc[masks['test'], 'date_id'].min())
        self.assertTrue((sum(m.astype(int) for m in masks.values()) == 1).all())

    def test_lag_resets_for_each_symbol_and_day(self):
        data = validate(synthetic())
        x = engineer(data)
        first = data.groupby(['date_id', 'symbol_id']).head(1).index
        self.assertTrue(x.loc[first, 'feature_00_lag1'].isna().all())
        row = data.index[(data.date_id == 0) & (data.time_id == 1) & (data.symbol_id == 0)][0]
        self.assertEqual(x.loc[row, 'feature_00_lag1'], data.loc[0, 'feature_00'])

    def test_future_feature_changes_do_not_change_past_features(self):
        data = synthetic()
        changed = data.copy()
        changed.loc[changed.date_id > 10, 'feature_00'] = 1e9
        pd.testing.assert_frame_equal(engineer(data).loc[data.date_id <= 10], engineer(changed).loc[data.date_id <= 10])

    def test_missing_flags_are_explicit(self):
        data = synthetic()
        data.loc[0, 'feature_00'] = np.nan
        self.assertEqual(engineer(data).loc[0, 'feature_00_missing'], 1.)

    def test_test_labels_are_never_used_or_exported(self):
        data = synthetic()
        changed = data.copy()
        changed.loc[changed.date_id >= 24, 'responder_6'] = np.nan
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/'a', Path(tmp)/'b'
            m1, _ = checkpoint(data, a, 'demo')
            m2, _ = checkpoint(changed, b, 'demo')
            pd.testing.assert_frame_equal(m1, m2)
            self.assertEqual((a/'predictions.csv').read_bytes(), (b/'predictions.csv').read_bytes())
            predictions = pd.read_csv(a/'predictions.csv')
            self.assertLess(predictions.date_id.max(), 24)
            self.assertNotIn('responder_6', predictions)

    def test_validation_values_do_not_change_training_model(self):
        data = synthetic()
        changed = data.copy()
        changed.loc[changed.date_id >= 18, 'feature_00'] = 1e6
        changed.loc[changed.date_id >= 18, 'responder_6'] = -1e6
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/'a', Path(tmp)/'b'
            checkpoint(data, a, 'demo')
            checkpoint(changed, b, 'demo')
            p1, p2 = pd.read_csv(a/'predictions.csv'), pd.read_csv(b/'predictions.csv')
            pd.testing.assert_frame_equal(p1[p1.split == 'train'], p2[p2.split == 'train'])

    def test_all_missing_training_column_is_dropped(self):
        data = synthetic()
        data.loc[data.date_id < 18, 'feature_00'] = np.nan
        with tempfile.TemporaryDirectory() as tmp:
            _, manifest = checkpoint(data, tmp, 'demo')
            self.assertNotIn('feature_00', manifest['features'])
            self.assertIn('feature_00_missing', manifest['features'])

    def test_demo_real_output_collision_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint(synthetic(), tmp, 'demo')
            with self.assertRaisesRegex(ValueError, 'mix'):
                checkpoint(synthetic(), tmp, 'real')

    def test_prepare_retains_complete_selected_groups(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'raw.csv', Path(tmp)/'slice.csv'
            synthetic().to_csv(source, index=False)
            manifest = prepare(source, out, 0, 19, [0, 1])
            self.assertEqual(manifest['rows'], 20*12*2)
            self.assertEqual(pd.read_csv(out).groupby(['date_id','symbol_id']).size().unique().tolist(), [12])
            self.assertEqual(len(json.loads(out.with_suffix('.manifest.json').read_text())['output_sha256']), 64)

    def test_row_cap_fails_without_partial_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'raw.csv', Path(tmp)/'slice.csv'
            synthetic().to_csv(source, index=False)
            with self.assertRaisesRegex(ValueError, 'row cap'):
                prepare(source, out, 0, 29, [0, 1, 2], 20)
            self.assertFalse(out.exists())

    def test_source_inspection_reports_schema_and_identifiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'source.csv'
            synthetic().to_csv(source, index=False)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                inspect(source)
            metadata = json.loads(buffer.getvalue().split('Counts per date/symbol')[0])
            self.assertEqual(metadata['rows'], 1080)
            self.assertEqual(metadata['symbols'], [0, 1, 2])
            self.assertEqual(len(metadata['dates']), 30)

    def test_cli_rejects_slice_changed_after_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, prepared = Path(tmp)/'raw.csv', Path(tmp)/'slice.csv'
            synthetic().to_csv(source, index=False)
            prepare(source, prepared, 0, 29, [0, 1])
            with prepared.open('a') as handle:
                handle.write('\n')
            command = [sys.executable, str(Path(__file__).resolve().parents[1]/'scripts/run_forecasting.py'),
                       '--input', str(prepared), '--output', str(Path(tmp)/'out')]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('changed since its manifest', result.stderr)
            self.assertFalse((Path(tmp)/'out').exists())

    def test_parquet_selection_matches_csv(self):
        try:
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest('Optional Parquet engine not installed')
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'raw.parquet', Path(tmp)/'slice.csv'
            synthetic().to_parquet(source)
            manifest = prepare(source, out, 0, 19, [0, 1])
            self.assertEqual(manifest['rows'], 480)


if __name__ == '__main__':
    unittest.main()
