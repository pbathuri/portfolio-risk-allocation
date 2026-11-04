"""Fetch official monthly value-weighted industry returns, with provenance."""
from pathlib import Path
import requests,zipfile,io,re,hashlib,json,datetime
import pandas as pd
url='https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip'
r=requests.get(url,timeout=90);r.raise_for_status()
z=zipfile.ZipFile(io.BytesIO(r.content));name=next(n for n in z.namelist() if n.lower().endswith('.csv'))
lines=z.read(name).decode('utf-8-sig').splitlines()
start=next(i for i,line in enumerate(lines) if 'Average Value Weighted Returns -- Monthly' in line)
header=None;rows=[]
for line in lines[start+1:]:
    if header is None:
        if line.strip().startswith(','):header=line;continue
    elif re.match(r'^\s*\d{6},',line):rows.append(line)
    elif rows:break
if header is None or not rows:raise ValueError('Upstream format changed: inspect source')
x=pd.read_csv(io.StringIO('\n'.join([header]+rows)));x.columns=['date']+[s.strip() for s in x.columns[1:]]
x['date']=pd.to_datetime(x.date.astype(str),format='%Y%m')+pd.offsets.MonthEnd(0)
x=x.melt('date',var_name='asset',value_name='ret');x['ret']=pd.to_numeric(x.ret,errors='raise')
x.loc[x.ret.isin([-99.99,-999]),'ret']=float('nan');x['ret']/=100
x=x[(x.date>='2010-01-01')&(x.date<='2025-12-31')]
out=Path(__file__).resolve().parents[1]/'data/raw';out.mkdir(parents=True,exist_ok=True)
(out/'french_source.zip').write_bytes(r.content);x.to_csv(out/'returns.csv',index=False)
(out/'french_provenance.json').write_text(json.dumps({'url':url,'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(r.content).hexdigest(),'section':'Average Value Weighted Returns -- Monthly','units':'decimal returns; converted from percent'},indent=2))
print(x.shape,'rows/columns; check source rights before redistributing')
