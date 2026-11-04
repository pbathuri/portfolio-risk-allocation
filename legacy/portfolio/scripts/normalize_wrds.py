import argparse,hashlib,json
from pathlib import Path
import pandas as pd
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--date',required=True);p.add_argument('--asset',required=True);p.add_argument('--ret',required=True);a=p.parse_args()
x=pd.read_csv(a.input);x=x[[a.date,a.asset,a.ret]].rename(columns={a.date:'date',a.asset:'asset',a.ret:'ret'})
x['date']=pd.to_datetime(x.date,errors='raise').dt.to_period('M').dt.to_timestamp('M')
x['ret']=pd.to_numeric(x.ret,errors='raise')
assert x.asset.notna().all() and np.isfinite(x.ret).all() and (x.ret>=-1).all()
assert not x.duplicated(['date','asset']).any()
out=Path(__file__).resolve().parents[1]/'data/raw';out.mkdir(parents=True,exist_ok=True)
x.sort_values(['date','asset']).to_csv(out/'returns.csv',index=False)
(out/'wrds_import.json').write_text(json.dumps({'source_sha256':hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),'columns':vars(a),'note':'Caller must verify total-return and delisting definition'},indent=2))
print('Wrote canonical returns. Review universe, missingness and source terms before use.')
