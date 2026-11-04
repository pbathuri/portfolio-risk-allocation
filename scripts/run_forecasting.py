"""Run a development checkpoint; intentionally no final-test evaluation option."""
from pathlib import Path
import argparse
import json
import sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from forecasting import checkpoint, file_hash, synthetic


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--demo', action='store_true')
    source.add_argument('--input', type=Path, help='Prepared checkpoint CSV')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    mode = 'demo' if args.demo else 'real'
    frame = synthetic() if args.demo else pd.read_csv(args.input, nrows=500001)
    if len(frame) > 500000:
        parser.error('Input exceeds the 500,000-row checkpoint cap; prepare a smaller complete-group slice')
    provenance = {'kind': 'synthetic', 'seed': 42} if args.demo else {
        'file': args.input.name, 'sha256': file_hash(args.input)}
    if args.input:
        preparation = args.input.with_suffix('.manifest.json')
        if preparation.exists():
            metadata = json.loads(preparation.read_text())
            if metadata.get('output_sha256') != provenance['sha256']:
                parser.error('Prepared input changed since its manifest; regenerate the slice')
            provenance['preparation'] = metadata
    output = args.output or Path('outputs') / mode
    metrics, manifest = checkpoint(frame, output, mode, provenance)
    print(metrics.to_string(index=False))
    print(f'Artifacts: {output}; final test: {manifest["test_status"]}')


if __name__ == '__main__':
    main()
