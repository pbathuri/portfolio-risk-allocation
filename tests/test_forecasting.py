from pathlib import Path
from contextlib import redirect_stdout
import io
import sys
import json
import tempfile
import unittest
from unittest.mock import patch,Mock
import subprocess
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from forecasting import validate,engineer,synthetic,split_dates,checkpoint,weighted_metrics
from prepare_forecasting import prepare
from fetch_data import fetch


class ForecastingTests(unittest.TestCase):
    def test_metric_hand_calculation(self):
        m=weighted_metrics([1,2],[0,1],[1,3])
        self.assertAlmostEqual(m['weighted_rmse'],1)
        self.assertAlmostEqual(m['weighted_zero_mean_r2'],1-4/13)

    def test_undefined_r2(self):
        self.assertIsNone(weighted_metrics([0],[1],[1])['weighted_zero_mean_r2'])

    def test_invalid_weights(self):
        for w in [[0,0],[-1,2],[np.nan,1]]:
            with self.subTest(w=w),self.assertRaises(ValueError):
                weighted_metrics([1,2],[1,2],w)

    def test_duplicate_date_rejected(self):
        data=synthetic()
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            validate(pd.concat([data,data.iloc[:1]]))

    def test_source_date_format(self):
        data=synthetic()
        data.date=pd.to_datetime(data.date).dt.strftime('%d-%b-%y')
        self.assertEqual(validate(data).date.iloc[0],pd.Timestamp('2020-01-01'))

    def test_lags_and_rolling_end_two_rows_back(self):
        data=synthetic();data.SP=np.arange(len(data),dtype=float)
        x=engineer(data)
        self.assertEqual(x.loc[21,'SP_lag2'],19)
        self.assertEqual(x.loc[21,'SP_mean20_lag2'],9.5)
        self.assertAlmostEqual(x.loc[21,'SP_std20_lag2'],np.std(np.arange(20),ddof=1))

    def test_current_and_future_values_do_not_change_current_features(self):
        data=synthetic(); changed=data.copy()
        changed.loc[39:,'SP']=999
        pd.testing.assert_frame_equal(engineer(data).loc[:40],engineer(changed).loc[:40])

    def test_missingness_flag_tracks_lagged_input(self):
        data=synthetic();data.loc[30,'DAX']=np.nan
        self.assertEqual(engineer(data).loc[32,'DAX_lag2_missing'],1)

    def test_warmup_and_splits_do_not_overlap(self):
        data=validate(synthetic());m=split_dates(data)
        self.assertFalse(sum(m.values())[:21].any())
        self.assertTrue((sum(m.values())[21:]==1).all())
        self.assertLess(data.loc[m['train'],'date'].max(),data.loc[m['validation'],'date'].min())
        self.assertLess(data.loc[m['validation'],'date'].max(),data.loc[m['test'],'date'].min())

    def test_test_targets_not_used_or_exported(self):
        data=synthetic();changed=data.copy();changed.loc[split_dates(data)['test'],'SP']=np.nan
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/'a',Path(tmp)/'b'
            m1,manifest=checkpoint(data,a,'demo');m2,_=checkpoint(changed,b,'demo')
            pd.testing.assert_frame_equal(m1,m2)
            self.assertEqual((a/'predictions.csv').read_bytes(),(b/'predictions.csv').read_bytes())
            self.assertEqual(manifest['test_status'],'withheld; not scored')
            self.assertEqual(set(pd.read_csv(a/'predictions.csv').split),{'train','validation'})

    def test_validation_does_not_change_training_fit(self):
        data=synthetic();changed=data.copy();changed.loc[~split_dates(data)['train'] & (np.arange(len(data))>=21),'SP']=999
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/'a',Path(tmp)/'b'
            m1,_=checkpoint(data,a,'demo');m2,_=checkpoint(changed,b,'demo')
            pd.testing.assert_frame_equal(m1[m1.split=='train'],m2[m2.split=='train'])

    def test_all_missing_training_feature_dropped(self):
        data=synthetic();data['DAX']=np.nan
        with tempfile.TemporaryDirectory() as tmp:
            _,m=checkpoint(data,tmp,'demo')
            self.assertNotIn('DAX_lag2',m['features'])

    def test_mode_collision_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint(synthetic(),tmp,'demo')
            with self.assertRaisesRegex(ValueError,'mix'):
                checkpoint(synthetic(),tmp,'real')

    def test_preparation_preserves_returns(self):
        with tempfile.TemporaryDirectory() as tmp:
            src,out=Path(tmp)/'raw.csv',Path(tmp)/'prepared.csv'
            data=synthetic();data.to_csv(src,index=False);m=prepare(src,out)
            self.assertEqual(m['rows'],len(data))
            np.testing.assert_allclose(pd.read_csv(out).SP,data.SP)
            self.assertEqual(len(m['source_sha256']),64)

    def test_changed_prepared_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            src,out=Path(tmp)/'raw.csv',Path(tmp)/'prepared.csv'
            synthetic().to_csv(src,index=False);prepare(src,out)
            with out.open('a') as f:f.write('\n')
            r=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'scripts/run_forecasting.py'),'--input',str(out),'--output',str(Path(tmp)/'result')],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertIn('changed since its manifest',r.stderr)

    def test_download_validates_before_writing(self):
        response=Mock();response.content=b'<html>not a csv</html>'
        with tempfile.TemporaryDirectory() as tmp,patch('fetch_data.requests.get',return_value=response):
            path=Path(tmp)/'source.csv'
            with self.assertRaises(ValueError):fetch(path)
            self.assertFalse(path.exists())

    def test_download_saves_valid_source_bytes(self):
        response=Mock();response.content=synthetic().to_csv(index=False).encode()
        with tempfile.TemporaryDirectory() as tmp,patch('fetch_data.requests.get',return_value=response),redirect_stdout(io.StringIO()):
            path=Path(tmp)/'source.csv';fetch(path)
            self.assertEqual(path.read_bytes(),response.content)


if __name__=='__main__':unittest.main()
