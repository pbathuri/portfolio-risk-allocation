"""Download the openly licensed UCI CSV; no account or API key required."""
from pathlib import Path
import argparse
import sys
import requests
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from forecasting import SOURCE_URL, file_hash, validate
import pandas as pd
from io import BytesIO


def fetch(output):
    output=Path(output)
    response=requests.get(SOURCE_URL,timeout=60)
    response.raise_for_status()
    if len(response.content)>2_000_000:
        raise ValueError('Unexpected source size; inspect before proceeding')
    frame=validate(pd.read_csv(BytesIO(response.content)))
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(response.content)
    print(f'Downloaded {len(response.content)} bytes, {len(frame)} rows to {output}')
    print('SHA256:',file_hash(output))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('data/raw/uci_istanbul.csv'))
    fetch(parser.parse_args().output)
