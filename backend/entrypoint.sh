#!/bin/sh
# Apply Alembic migrations before starting the application server.
# Resolves NM-049: Docker API container did not run migrations at startup,
# causing 500 errors on first request after a clean docker compose up.
set -e
alembic upgrade head
exec "$@"
