"""Inspect identifiers/schema of one local source, without summarizing targets."""
from pathlib import Path
import argparse
import json
import pandas as pd


def inspect(path):
    path = Path(path)
    keys = ['date_id', 'symbol_id']
    if path.suffix.lower() == '.csv':
        columns = pd.read_csv(path, nrows=0).columns.tolist()
        batches = pd.read_csv(path, usecols=keys, chunksize=50000)
    elif path.suffix.lower() == '.parquet':
        import pyarrow.parquet as pq
        source = pq.ParquetFile(path)
        columns = source.schema_arrow.names
        batches = (b.to_pandas() for b in source.iter_batches(columns=keys, batch_size=50000))
    else:
        raise ValueError('Expected CSV or Parquet')
    counts = None
    try:
        for batch in batches:
            group = batch.groupby(keys).size()
            counts = group if counts is None else counts.add(group, fill_value=0)
    finally:
        if hasattr(batches, 'close'):
            batches.close()
    if counts is None or counts.empty:
        raise ValueError('No source rows')
    print(json.dumps({'file': path.name, 'columns': columns, 'rows': int(counts.sum()),
                      'dates': sorted(map(int, counts.index.get_level_values('date_id').unique())),
                      'symbols': sorted(map(int, counts.index.get_level_values('symbol_id').unique()))}, indent=2))
    print('Counts per date/symbol (first 30 groups):')
    print(counts.astype(int).head(30).to_string())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    inspect(parser.parse_args().input)
