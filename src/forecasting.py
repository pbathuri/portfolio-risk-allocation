"""Chronological return-forecasting checkpoint on the CC BY 4.0 UCI dataset."""
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import pandas as pd
import sklearn
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

RETURNS = ['ISE', 'ISE.1', 'SP', 'DAX', 'FTSE', 'NIKKEI', 'BOVESPA', 'EU', 'EM']
TARGET = 'SP'
SOURCE_URL = 'https://archive.ics.uci.edu/static/public/247/data.csv'
SOURCE_PAGE = 'https://archive.ics.uci.edu/dataset/247/istanbul+stock+exchange'
LICENSE = 'https://creativecommons.org/licenses/by/4.0/'


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate(frame):
    missing = set(['date'] + RETURNS) - set(frame.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    frame = frame[['date'] + RETURNS].copy()
    # ISO dates are prepared files; the publisher uses 5-Jan-09.
    dates = frame['date'].astype(str)
    fmt = '%Y-%m-%d' if dates.str.match(r'^\d{4}-\d{2}-\d{2}$').all() else '%d-%b-%y'
    frame['date'] = pd.to_datetime(dates, format=fmt, errors='raise')
    if frame.date.duplicated().any():
        raise ValueError('Duplicate dates')
    frame[RETURNS] = frame[RETURNS].apply(pd.to_numeric, errors='raise')
    if np.isinf(frame[RETURNS].to_numpy()).any():
        raise ValueError('Infinite returns are invalid')
    if len(frame) < 50:
        raise ValueError('At least 50 observations required')
    return frame.sort_values('date').reset_index(drop=True)


def engineer(frame):
    """Predict SP at row t using only information at or before row t-2."""
    frame = validate(frame)
    x = frame[RETURNS].shift(2).add_suffix('_lag2')
    for window in [5, 20]:
        x[f'SP_mean{window}_lag2'] = frame.SP.shift(2).rolling(window, min_periods=window).mean()
        x[f'SP_std{window}_lag2'] = frame.SP.shift(2).rolling(window, min_periods=window).std(ddof=1)
    for col in list(x):
        x[col + '_missing'] = x[col].isna().astype(float)
    return x


def split_dates(frame):
    """Remove fixed 21-row warm-up, then split dates 60/20/20; no overlap."""
    n = len(frame) - 21
    if n < 25:
        raise ValueError('Insufficient observations after warm-up')
    a, b = 21 + int(.6*n), 21 + int(.8*n)
    idx = np.arange(len(frame))
    return {'train': (idx >= 21) & (idx < a), 'validation': (idx >= a) & (idx < b),
            'test': idx >= b}


def weighted_metrics(y, prediction, weight):
    y, prediction, weight = [np.asarray(v, dtype=float) for v in (y, prediction, weight)]
    if y.shape != prediction.shape or y.shape != weight.shape or y.ndim != 1:
        raise ValueError('Metrics require equally sized vectors')
    if not all(np.isfinite(v).all() for v in (y, prediction, weight)) or (weight < 0).any():
        raise ValueError('Metrics require finite values and nonnegative weights')
    if weight.sum() <= 0:
        raise ValueError('Metric weights must have positive total')
    error = float(np.sum(weight*(y-prediction)**2))
    denominator = float(np.sum(weight*y**2))
    return {'weighted_rmse': float(np.sqrt(error/weight.sum())),
            'weighted_zero_mean_r2': None if denominator == 0 else 1-error/denominator}


def synthetic():
    rng = np.random.default_rng(42)
    frame = pd.DataFrame(rng.normal(0, .01, size=(160, len(RETURNS))), columns=RETURNS)
    frame.insert(0, 'date', pd.bdate_range('2020-01-01', periods=len(frame)).strftime('%Y-%m-%d'))
    return frame


def checkpoint(frame, output, mode, source=None):
    if mode not in {'demo', 'real'}:
        raise ValueError('Mode must be demo or real')
    out = Path(output)
    manifest_path = out/'manifest.json'
    if manifest_path.exists() and json.loads(manifest_path.read_text())['mode'] != mode:
        raise ValueError('Do not mix demo and real outputs')
    frame = validate(frame)
    masks, x = split_dates(frame), engineer(frame)
    train = masks['train']
    kept = x.columns[x.loc[train].notna().any()].tolist()
    x = x[kept]
    y = frame.loc[train, TARGET].to_numpy()
    weighted_metrics(y, np.zeros(len(y)), np.ones(len(y)))
    model = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), Ridge(alpha=1.0))
    model.fit(x.loc[train], y)
    mean = float(np.mean(y))
    results, predictions = [], []
    for name in ['train', 'validation']:
        mask = masks[name]
        actual = frame.loc[mask, TARGET]
        guesses = {'zero': np.zeros(mask.sum()), 'training_mean': np.full(mask.sum(), mean),
                   'persistence_lag2': frame[TARGET].shift(2).loc[mask].to_numpy(),
                   'ridge': model.predict(x.loc[mask])}
        for method, guess in guesses.items():
            results.append({'mode': mode, 'split': name, 'model': method, 'rows': int(mask.sum()),
                            **weighted_metrics(actual, guess, np.ones(mask.sum()))})
            predictions.append(pd.DataFrame({'date': frame.loc[mask,'date'].dt.strftime('%Y-%m-%d'),
                'split': name, 'model': method, 'prediction': guess}))
    splits = {name: {'rows': int(mask.sum()), 'start': frame.loc[mask,'date'].min().date().isoformat(),
                    'end': frame.loc[mask,'date'].max().date().isoformat()} for name,mask in masks.items()}
    manifest = {'mode': mode, 'source': source, 'python': platform.python_version(),
        'numpy': np.__version__, 'pandas': pd.__version__, 'sklearn': sklearn.__version__,
        'splits': splits, 'features': kept, 'ridge_alpha': 1., 'warmup_rows': 21,
        'target': 'SP return on observation date', 'weight': 'equal weight; ones',
        'test_status': 'withheld; not scored', 'lag_contract': 'all predictors end at row t-2; rows are not uniform calendar intervals'}
    out.mkdir(parents=True,exist_ok=True)
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    pd.DataFrame(results).to_csv(out/'metrics.csv',index=False)
    pd.concat(predictions).to_csv(out/'predictions.csv',index=False)
    dev = masks['train'] | masks['validation']
    pd.DataFrame({'feature': kept, 'missing_fraction': x.loc[dev].isna().mean().to_numpy()}).to_csv(out/'missingness.csv',index=False)
    pd.DataFrame({'feature':kept,'definition':[
        'missingness indicator of lagged input' if col.endswith('_missing') else
        'rolling statistic ending at t-2' if 'mean' in col or 'std' in col else
        'published return two observed rows earlier' for col in kept]}).to_csv(out/'feature_catalog.csv',index=False)
    return pd.DataFrame(results),manifest
