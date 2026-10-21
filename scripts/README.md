# Profile assets

- `build.py` renders every static asset in `assets/` and writes `README.md`. Edit the text in `build.py`, then run `pip install fonttools uharfbuzz && python scripts/build.py`.
- `stats.py` renders the activity card from the GitHub GraphQL API. The `Profile activity` workflow runs it every day and publishes the result to the `output` branch.

Text is converted to outlines with Inter (`fonts/`, SIL Open Font License) so the cards look the same on every device.
