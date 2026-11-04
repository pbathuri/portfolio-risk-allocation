"""Validate UCI's published CSV and preserve all observations and provenance."""
from pathlib import Path
import argparse
import json
import sys
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from forecasting import validate, file_hash, SOURCE_URL, SOURCE_PAGE, LICENSE


def prepare(source, output):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve():
        raise ValueError('Output must differ from source')
    frame=validate(pd.read_csv(source))
    output.parent.mkdir(parents=True,exist_ok=True)
    frame.to_csv(output,index=False,date_format='%Y-%m-%d')
    manifest={'source_file':source.name,'source_url':SOURCE_URL,'source_page':SOURCE_PAGE,
        'license':LICENSE,'attribution':'Akbilgic, O. (2013). ISTANBUL STOCK EXCHANGE. UCI. DOI:10.24432/C54P4J',
        'source_sha256':file_hash(source),'output_sha256':file_hash(output),'rows':len(frame),
        'start':frame.date.min().date().isoformat(),'end':frame.date.max().date().isoformat(),
        'changes':'Parsed dates to ISO, sorted dates; no raw observations dropped or returns changed.'}
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('data/raw/uci_istanbul.csv'))
    parser.add_argument('--output',type=Path,default=Path('data/processed/checkpoint.csv'))
    args=parser.parse_args()
    print(json.dumps(prepare(args.input,args.output),indent=2))
