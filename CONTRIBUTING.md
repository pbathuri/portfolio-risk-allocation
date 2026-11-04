# Contributing

Use a short branch such as `week-1/lag-comparison` and open a pull request with:

- The question or issue addressed.
- Commands needed to reproduce the result.
- Relevant tests and any limitations.

Ask the other team member to review the change. Each person should be able to explain the methods and reproduce the results. Keep reusable Python code in `src/` and assign one owner to each notebook while it is being edited.

Discuss changes to the data source, target, split dates or evaluation method before implementing them. Record research decisions in `docs/DECISIONS.md`.

Keep credentials and generated data out of Git. Cite data and code sources, retain applicable license notices, and distinguish measured results from proposed work. Run `python -m unittest discover -s tests` before submitting a code change.
