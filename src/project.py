"""Monthly total-return baseline; training, validation and test are separated by date."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
TRAIN_END='2018-12-31'; VALID_END='2021-12-31'; TEST_END='2025-12-31'

def load_data(mode='demo'):
    if mode=='demo':
        rng=np.random.default_rng(42); dates=pd.date_range('2010-01-31',periods=192,freq='ME')
        common=rng.normal(.005,.025,(len(dates),1)); values=common+rng.normal(.001,.025,(len(dates),6))
        return pd.DataFrame(values,index=dates,columns=[f'DEMO_ASSET_{i}' for i in range(6)]).rename_axis('date')
    if mode!='real':raise ValueError('mode must be demo or real')
    x=pd.read_csv(ROOT/'data/raw/returns.csv',parse_dates=['date'])
    if x.duplicated(['date','asset']).any():raise ValueError('Duplicate date/asset')
    return x.pivot(index='date',columns='asset',values='ret').sort_index()

def preview(x):print(x.head().to_string())

def validate(x):
    assert len(x)>=120 and x.shape[1]>=2
    assert isinstance(x.index,pd.DatetimeIndex) and x.index.is_monotonic_increasing and x.index.is_unique
    periods=x.index.to_period('M')
    assert periods.is_unique and len(pd.period_range(periods.min(),periods.max(),freq='M'))==len(periods), 'Missing or duplicate months'
    assert np.isfinite(x.to_numpy()).all(), 'Resolve missing/non-numeric returns; do not fill with zero'
    assert (x>=-1).all().all(), 'Simple total return cannot be below -100%'
    return pd.DataFrame({'months':[len(x)],'assets':[x.shape[1]],'missing':[int(x.isna().sum().sum())]})

def split(x):
    validate(x)
    train=x.loc[:TRAIN_END]; valid=x.loc[(x.index>TRAIN_END)&(x.index<=VALID_END)]; test=x.loc[(x.index>VALID_END)&(x.index<=TEST_END)]
    assert len(train)>=60 and len(valid)>=12 and len(test)>=12, 'Insufficient dates for frozen split'
    return train,valid,test

def weights(train):
    n=train.shape[1];eq=np.ones(n)/n; cov=train.cov().to_numpy()*12
    vol=train.std(ddof=1).to_numpy()
    if (vol<=0).any():raise ValueError('Zero-variance asset')
    inv=1/vol;inv/=inv.sum()
    opt=minimize(lambda w:float(w@cov@w),eq,bounds=[(0,1)]*n,constraints=[{'type':'eq','fun':lambda w:w.sum()-1}],method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
    if not opt.success:raise RuntimeError(opt.message)
    return pd.DataFrame({'equal_weight':eq,'inverse_vol':inv,'min_variance':opt.x},index=train.columns).rename_axis('asset')

def allocation_cloud(train,n=5000,seed=42):
    rng=np.random.default_rng(seed);w=rng.dirichlet(np.ones(train.shape[1]),size=n)
    mu=train.mean().to_numpy()*12;cov=train.cov().to_numpy()*12
    out=pd.DataFrame({'portfolio_id':np.arange(n),'expected_return':w@mu,'expected_vol':np.sqrt(np.einsum('ij,jk,ik->i',w,cov,w)),
      'hhi':(w*w).sum(1)})
    long=pd.DataFrame(w,columns=train.columns).rename_axis('portfolio_id').reset_index().melt('portfolio_id',var_name='asset',value_name='weight')
    return out,long

def simulate(x,w,cost_bps=0):
    w=np.asarray(w,float)
    if not np.isfinite(w).all() or (w<0).any() or not np.isclose(w.sum(),1):raise ValueError('Invalid allocation')
    # Monthly reset to target. One-way turnover = half L1 distance from drifted holdings.
    drift=w.copy(); returns=[];turnovers=[]
    for row in x.to_numpy():
        turnover=.5*np.abs(w-drift).sum();gross=float(row@w)
        if gross<=-1:raise ValueError('Portfolio bankruptcy; wealth process undefined thereafter')
        net=(1-turnover*cost_bps/10000)*(1+gross)-1
        returns.append(net);turnovers.append(turnover)
        drift=w*(1+row)/(1+gross)
    return pd.Series(returns,index=x.index),np.array(turnovers)

def risk_metrics(r):
    wealth=np.r_[1,np.cumprod(1+r.to_numpy())]
    dd=wealth/np.maximum.accumulate(wealth)-1
    loss=-r.to_numpy();var=float(np.quantile(loss,.95));tail=loss[loss>=var]
    return dict(realized_ann_mean=r.mean()*12,realized_ann_vol=r.std(ddof=1)*np.sqrt(12),
       cagr=wealth[-1]**(12/len(r))-1,max_drawdown=float(dd.min()),monthly_var95=var,monthly_es95=float(tail.mean()))

def evaluate(x,w,cost_bps=0):
    rows=[];curves=[]
    for name in w:
        r,t=simulate(x,w[name],cost_bps)
        rows.append(dict(strategy=name,**risk_metrics(r),mean_monthly_turnover=t.mean(),cost_bps=cost_bps,months=len(x)))
        curves.extend(dict(date=str(dt.date()),strategy=name,wealth=float(v)) for dt,v in (1+r).cumprod().items())
    return pd.DataFrame(rows),pd.DataFrame(curves)

def block_bootstrap(x,w,seed=42,n=1000,block=6):
    r,_=simulate(x,w);a=r.to_numpy();rng=np.random.default_rng(seed);draws=[]
    for _ in range(n):
        starts=rng.integers(0,len(a),size=int(np.ceil(len(a)/block)))
        idx=np.concatenate([(s+np.arange(block))%len(a) for s in starts])[:len(a)]
        draws.append(a[idx].std(ddof=1)*np.sqrt(12))
    return pd.DataFrame({'seed':[seed],'block_months':[block],'vol_low':[np.quantile(draws,.025)],'vol_high':[np.quantile(draws,.975)]})

def export(x,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    train,valid,test=split(x);w=weights(train);w.to_csv(out/'weights.csv')
    cloud,long=allocation_cloud(train);cloud.to_csv(out/'portfolio_cloud.csv',index=False);long.to_csv(out/'portfolio_weights.csv',index=False)
    for period,data in [('validation',valid),('test',test)]:
        score,curves=evaluate(data,w,10)
        score.to_csv(out/f'{period}_metrics.csv',index=False);curves.to_csv(out/f'{period}_wealth.csv',index=False)
    train.corr().to_csv(out/'correlations.csv')
    fig,ax=plt.subplots(figsize=(7,5));ax.scatter(cloud.expected_vol,cloud.expected_return,c=cloud.hhi,s=4,cmap='viridis')
    ax.set(xlabel='Estimated annual volatility',ylabel='Estimated annual arithmetic return',title='Training estimates | feasible allocations, not an efficient frontier')
    fig.tight_layout();fig.savefig(out/'allocation_cloud.png',dpi=150);plt.close(fig)
    return w,cloud

def run_demo():
    export(load_data(),ROOT/'outputs/demo');print('SYNTHETIC portfolio demo complete')
