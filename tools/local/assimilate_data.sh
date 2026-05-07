#!/bin/bash
# Fix ownership of SCP-transferred .data so postgres/redis containers can access their volumes,
# then start the stack to resume the original database/cache state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$PROJECT_ROOT/.data"

if [ ! -d "$DATA_DIR" ]; then
    echo "ERROR: .data directory not found at $DATA_DIR"
    exit 1
fi

# postgres:17  → internal user 'postgres'  uid=999 gid=999
# postgres data dir must be mode 700 or postgres refuses to start
if [ -d "$DATA_DIR/postgres_data" ]; then
    echo "Fixing postgres_data ownership (999:999, mode 700)..."
    sudo chown -R 999:999 "$DATA_DIR/postgres_data"
    sudo chmod 700 "$DATA_DIR/postgres_data"
fi

# redis:7.2.4  → internal user 'redis'  uid=999 gid=999
if [ -d "$DATA_DIR/redis" ]; then
    echo "Fixing redis ownership (999:999)..."
    sudo chown -R 999:999 "$DATA_DIR/redis"
fi

echo "Starting services..."
docker compose -f "$PROJECT_ROOT/docker-compose.local.yml" up -d

echo "Done. Services are up with the restored data state."