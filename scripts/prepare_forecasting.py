"""Filter one local CSV/Parquet file; never silently truncate complete groups."""
from pathlib import Path
import argparse
import json
import sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from forecasting import COLUMNS, file_hash, split_dates, validate


def prepare(source, output, start, end, symbols, max_rows=500000):
    source, output = Path(source), Path(output)
    if start > end or max_rows < 1 or not symbols:
        raise ValueError('Require start <= end, positive max rows and symbols')
    if source.resolve() == output.resolve():
        raise ValueError('Output must differ from source')
    if source.suffix.lower() == '.csv':
        batches = pd.read_csv(source, usecols=COLUMNS, chunksize=50000)
    elif source.suffix.lower() == '.parquet':
        try:
            import pyarrow.parquet as pq
        except ImportError as exc:
            raise RuntimeError('Use the Kaggle notebook environment to export a bounded CSV, or an environment with pyarrow available') from exc
        batches = (batch.to_pandas() for batch in pq.ParquetFile(source).iter_batches(batch_size=50000, columns=COLUMNS))
    else:
        raise ValueError('Input must be one CSV or Parquet file')
    selected, count = [], 0
    try:
        for chunk in batches:
            subset = chunk.loc[chunk.date_id.between(start, end) & chunk.symbol_id.isin(symbols)]
            count += len(subset)
            if count > max_rows:
                raise ValueError('Selection exceeds row cap; narrow whole date/symbol groups, do not truncate rows')
            if len(subset):
                selected.append(subset)
    finally:
        if hasattr(batches, "close"):
            batches.close()
    if not selected:
        raise ValueError('No rows match the requested dates and symbols')
    frame = validate(pd.concat(selected, ignore_index=True))
    split_dates(frame)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    manifest = {'source_file': source.name, 'source_sha256': file_hash(source),
                'output_sha256': file_hash(output), 'rows': len(frame), 'columns': COLUMNS,
                'start_date_id': start, 'end_date_id': end, 'symbols': symbols,
                'scope': 'complete selected groups within supplied file only; verify source partition boundaries',
                'max_rows': max_rows}
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('data/processed/checkpoint.csv'))
    parser.add_argument('--start-date', type=int, required=True)
    parser.add_argument('--end-date', type=int, required=True)
    parser.add_argument('--symbols', type=int, nargs='+', required=True)
    parser.add_argument('--max-rows', type=int, default=500000)
    args = parser.parse_args()
    print(json.dumps(prepare(args.input, args.output, args.start_date, args.end_date, args.symbols, args.max_rows), indent=2))


if __name__ == '__main__':
    main()
