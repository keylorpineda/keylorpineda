# Profile assets

- `build_assets.py` renders the static cards in `assets/` (header, projects, toolbox, interests, certifications). Run it after editing any text: `pip install fonttools uharfbuzz && python scripts/build_assets.py`.
- `stats.py` renders the activity card from the GitHub GraphQL API. The `Profile activity` workflow runs it every day and publishes the result, together with the snake, to the `output` branch.

Text is converted to outlines with Inter (`fonts/`, SIL Open Font License) so the cards look the same on every device.
