# Shoonya DB Backup & Restore

All Shoonya data (datasets, projects, tasks, annotations, users, etc.) lives in the
PostgreSQL container `shoonya-backend-db`. Redis does **not** need a backup —
it only holds Celery queue/cache state.

This guide covers:

1. Taking a full database dump
2. Copying it off the host (optional)
3. Restoring the dump later

---

## Prerequisites

- Docker stack is running locally (`docker compose -f docker-compose.local.yml up -d`).
- Postgres container name: `shoonya-backend-db`
- DB name: `main`
- DB user: `admin`

---

## 1. Take a Dump

From the project root on the host:

```bash
mkdir -p backups
TS=$(date +%Y%m%d_%H%M%S)

# Create dump inside the container (custom format, compressed)
docker exec -t shoonya-backend-db \
  pg_dump -U admin -d main --no-owner --no-acl \
  -F c -f /tmp/shoonya_${TS}.dump

# Copy dump from container to host
docker cp shoonya-backend-db:/tmp/shoonya_${TS}.dump ./backups/shoonya_${TS}.dump

# Clean up dump inside container
docker exec shoonya-backend-db rm /tmp/shoonya_${TS}.dump

# Verify
ls -lh backups/
```

You should now have:

```
backups/shoonya_<TIMESTAMP>.dump
```

This single file contains the full database state.

---

## 2. (Optional) Move Dump to a Server

```bash
scp backups/shoonya_<TIMESTAMP>.dump user@your-server:/path/to/backups/
```

Or push to S3/any object store you use.

---

## 3. Restore From a Dump

Use this when you’ve deleted data via UI / DB and want to bring it back.

### 3.1 Copy dump into the Postgres container

```bash
docker cp ./backups/shoonya_<TIMESTAMP>.dump shoonya-backend-db:/tmp/dump.dump
```

### 3.2 Restore into the existing `main` database

```bash
docker exec -it shoonya-backend-db \
  pg_restore -U admin -d main \
  --no-owner --no-acl \
  --clean --if-exists \
  /tmp/dump.dump
```

Flags explained:

- `--clean --if-exists` → drops existing tables/rows first, then reloads from dump.
- `--no-owner --no-acl` → ignores ownership/ACL mismatches.

### 3.3 Remove dump from inside container

```bash
docker exec shoonya-backend-db rm /tmp/dump.dump
```

### 3.4 Restart web + celery so they pick up restored state

```bash
docker compose -f docker-compose.local.yml restart web celery celery2
```

### 3.5 Verify

Quick row count check:

```bash
docker exec -it shoonya-backend-db psql -U admin -d main -c \
  "SELECT count(*) FROM dataset_speechconversation;"
```

Or open the frontend → Datasets / Projects → your old data should appear.

---

## Notes

- The `.data/` folder in the project root is the bind-mounted Postgres data
  directory. The dump file above is independent of `.data/` and is the safe,
  portable way to back up.
- Redis (`shoonya-redis`) is not backed up here; it only carries Celery
  state which is rebuildable.
- Keep dump files in a separate, version-controlled or cloud-backed location
  (not inside the repo), so a clone/clean of the project never deletes them.
