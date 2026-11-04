"""Inspect source schema and dates without previewing final targets."""
from pathlib import Path
import argparse
import sys
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from forecasting import validate,split_dates

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',default='data/raw/uci_istanbul.csv')
    args=parser.parse_args()
    frame=validate(pd.read_csv(args.input))
    print('Rows:',len(frame),'Columns:',frame.columns.tolist())
    for name,mask in split_dates(frame).items():
        print(name,int(mask.sum()),frame.loc[mask,'date'].min().date(),frame.loc[mask,'date'].max().date())
