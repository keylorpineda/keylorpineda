# Profile assets

- `build.py` renders every static asset in `assets/` and writes `README.md`. Edit the text in `build.py`, then run `pip install fonttools uharfbuzz && python scripts/build.py`.
- `stats.py` renders the activity card from the GitHub GraphQL API. The `Profile activity` workflow runs it every day and publishes the result to the `output` branch.

Text is converted to outlines so the cards look the same on every device: Inter for body text and Bricolage Grotesque for display (`fonts/`, both under the SIL Open Font License). The palette in `svglib.py` matches keylorpineda.dev.
