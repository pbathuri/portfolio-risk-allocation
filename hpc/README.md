# Compute scope

The pre-Saturday checkpoint is CPU-first and runs locally or in an authorized Kaggle notebook. No GPU, cluster allocation or distributed training is needed. Measure time/memory on the bounded slice before requesting more resources.

A real cluster job is optional later if the team has access. Record machine, environment, input hashes, elapsed runtime and requested/used resources in `docs/RUN_LOG.csv`. Do not claim a cluster run if only a laptop run occurred. The archived portfolio Slurm examples in `legacy/portfolio/hpc/` are not jobs for this new forecasting pipeline and require adaptation before use.
