"""Small chronological forecasting checkpoint; final test labels are never scored."""
from pathlib import Path
import hashlib
import json
import platform

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

KEYS = ['date_id', 'time_id', 'symbol_id']
FEATURES = [f'feature_{i:02d}' for i in range(10)]
TARGET = 'responder_6'
COLUMNS = KEYS + ['weight'] + FEATURES + [TARGET]


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate(frame):
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    if frame.empty:
        raise ValueError('No selected rows')
    if frame.duplicated(KEYS).any():
        raise ValueError('Duplicate date/time/symbol keys')
    for col in KEYS:
        values = frame[col].to_numpy(dtype=float)
        if not np.isfinite(values).all() or (values < 0).any() or (values % 1 != 0).any():
            raise ValueError(f'{col} must contain nonnegative integer identifiers')
    weights = frame.weight.to_numpy(dtype=float)
    if not np.isfinite(weights).all() or (weights < 0).any():
        raise ValueError('Weights must be finite and nonnegative')
    # Test targets may be missing: validation never inspects their values.
    if np.isinf(frame[FEATURES].to_numpy(dtype=float)).any():
        raise ValueError('Infinite features are invalid; missing values may be NaN')
    return frame.sort_values(KEYS).reset_index(drop=True)


def split_dates(frame):
    dates = np.sort(frame.date_id.unique())
    if len(dates) < 10:
        raise ValueError('Select at least 10 distinct dates; 30 or more recommended')
    a, b = int(.6 * len(dates)), int(.8 * len(dates))
    return {name: frame.date_id.isin(ids) for name, ids in
            [('train', dates[:a]), ('validation', dates[a:b]), ('test', dates[b:])]}


def engineer(frame):
    """Past observed feature only; reset lags across symbols AND dates."""
    frame = validate(frame)
    x = frame[FEATURES].copy()
    for col in FEATURES:
        x[col + '_missing'] = frame[col].isna().astype(float)
    for col in FEATURES[:3]:
        x[col + '_lag1'] = frame.groupby(['date_id', 'symbol_id'])[col].shift(1)
    return x


def weighted_metrics(y, prediction, weight):
    y, prediction, weight = [np.asarray(v, dtype=float) for v in (y, prediction, weight)]
    if y.shape != prediction.shape or y.shape != weight.shape or y.ndim != 1:
        raise ValueError('Metrics require equally sized vectors')
    if not all(np.isfinite(v).all() for v in (y, prediction, weight)) or (weight < 0).any():
        raise ValueError('Metrics require finite values and nonnegative weights')
    total = weight.sum()
    if total <= 0:
        raise ValueError('Metric weights must have positive total')
    error = float(np.sum(weight * (y - prediction) ** 2))
    denominator = float(np.sum(weight * y ** 2))
    return {'weighted_rmse': float(np.sqrt(error / total)),
            'weighted_zero_mean_r2': None if denominator == 0 else 1 - error / denominator}


def synthetic():
    rng = np.random.default_rng(42)
    rows = []
    for day in range(30):
        for tick in range(12):
            for symbol in [0, 1, 2]:
                x = rng.normal(size=10)
                y = .3 * x[0] - .2 * x[1] + rng.normal(scale=.6)
                x[rng.random(10) < .04] = np.nan
                rows.append([day, tick, symbol, 1., *x, y])
    return pd.DataFrame(rows, columns=COLUMNS)


def checkpoint(frame, output, mode, source=None):
    if mode not in {'demo', 'real'}:
        raise ValueError('Mode must be demo or real')
    frame = validate(frame)
    masks = split_dates(frame)
    x = engineer(frame)
    train = masks['train']
    # Exclude all-missing training features before sklearn preprocessing.
    kept = x.columns[x.loc[train].notna().any()].tolist()
    x = x[kept]
    if not kept:
        raise ValueError('No usable training features')
    y = frame.loc[train, TARGET].to_numpy(dtype=float)
    w = frame.loc[train, 'weight'].to_numpy(dtype=float)
    weighted_metrics(y, np.zeros(len(y)), w)
    model = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), Ridge(alpha=1.0))
    model.fit(x.loc[train], y, ridge__sample_weight=w)
    mean = float(np.average(y, weights=w))
    results, predictions = [], []
    for name in ['train', 'validation']:
        mask = masks[name]
        actual, weights = frame.loc[mask, TARGET], frame.loc[mask, 'weight']
        guesses = {'zero': np.zeros(mask.sum()), 'training_mean': np.full(mask.sum(), mean),
                   'ridge': model.predict(x.loc[mask])}
        for method, guess in guesses.items():
            results.append({'mode': mode, 'split': name, 'model': method,
                            'rows': int(mask.sum()), **weighted_metrics(actual, guess, weights)})
            block = frame.loc[mask, KEYS].copy()
            block['split'], block['model'], block['prediction'] = name, method, guess
            predictions.append(block)
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / 'manifest.json'
    if manifest_path.exists() and json.loads(manifest_path.read_text())['mode'] != mode:
        raise ValueError('Do not mix demo and real outputs; choose a separate directory')
    splits = {name: {'rows': int(mask.sum()), 'dates': sorted(map(int, frame.loc[mask, 'date_id'].unique()))}
              for name, mask in masks.items()}
    manifest = {'mode': mode, 'source': source, 'python': platform.python_version(),
                'numpy': np.__version__, 'pandas': pd.__version__, 'splits': splits,
                'features': kept, 'ridge_alpha': 1.0, 'test_status': 'withheld; not scored',
                'lag_contract': 'previous observed row within same symbol and date; not fixed elapsed time'}
    import sklearn
    manifest['sklearn'] = sklearn.__version__
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    pd.DataFrame(results).to_csv(out / 'metrics.csv', index=False)
    pd.concat(predictions).to_csv(out / 'predictions.csv', index=False)
    # QA on development data only, to avoid browsing test distributions.
    dev = frame.loc[masks['train'] | masks['validation']]
    pd.DataFrame({'column': FEATURES, 'missing_fraction': dev[FEATURES].isna().mean().to_numpy()}).to_csv(out / 'missingness.csv', index=False)
    pd.DataFrame({'feature': kept, 'definition': [
        'previous observed same-symbol same-day value' if c.endswith('_lag1') else
        '1 if current raw value missing, else 0' if c.endswith('_missing') else
        'provided contemporaneous input; semantics anonymized' for c in kept]}).to_csv(out / 'feature_catalog.csv', index=False)
    return pd.DataFrame(results), manifest
