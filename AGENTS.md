# Repository Guidelines

## Project Structure & Module Organization
- `app/`: FastAPI app (`main.py`, `search.py`), `templates/` (Jinja2), `static/` assets.
- `scraper/`: data ingestion (`scrape_and_index.py`).
- Root: `Dockerfile`, `Dockerfile.scraper`, `docker-compose.yml`, `requirements.txt`.
- Assets live under `app/static/`; HTML under `app/templates/`.

## Build, Test, and Development Commands
- Build and run stack: `docker-compose up -d --build` — starts FastAPI, Elasticsearch, Kibana.
- Seed data: `docker-compose run --rm scraper` — fetches sample products and indexes them.
- Tail logs (web): `docker-compose logs -f web`; stop/clean: `docker-compose down -v`.
- Local dev (without Compose): `ELASTICSEARCH_URL=http://localhost:9200 uvicorn app.main:app --reload`.

## Coding Style & Naming Conventions
- Python 3.11, PEP 8, 4-space indent; prefer type hints for new code.
- Modules/functions: `snake_case`; classes: `PascalCase`; constants: `UPPER_SNAKE_CASE`.
- Templates: Jinja2 with small, composable partials (e.g., `_results.html`).

## Testing Guidelines
- No tests yet. If adding, use `pytest` and FastAPI `TestClient`.
- Place tests in `tests/`, name files `test_*.py`. Use a temporary ES index (e.g., `ES_INDEX=test_products`) and clean up after.

## Commit & Pull Request Guidelines
- Commits: imperative, concise, and scoped (e.g., "add search fuzziness", "fix scraper timeout"). Conventional Commits are welcome.
- PRs: clear description, what/why, steps to run, screenshots of UI when relevant, and linked issues.
- Verify `docker-compose up -d` succeeds and the scraper indexes data before requesting review.

## Security & Configuration Tips
- Configuration via env: `ELASTICSEARCH_URL`, `ES_INDEX`. Keep secrets in `.env` (already gitignored).
- Do not commit credentials or sample data with PII.
- When changing ES mappings, consider `docker-compose down -v` to reset local data.

