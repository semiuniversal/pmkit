## Official Docker Setup

The primary image is `openproject/openproject` (e.g., tag `:17` for the latest stable). It comes in two flavors:

- **All-in-one**: Quick-start with built-in DB and cache—ideal for testing or small setups.
- **Slim**: App-only, for production behind your own proxy/DB.

**Quick-start command** (runs on `localhost:8080`, admin/admin login):

```
textdocker run -it -p 8080:80 \
  -e SECRET_KEY_BASE=secret \
  -e OPENPROJECT_HOST__NAME=localhost:8080 \
  -e OPENPROJECT_HTTPS=false \
  -e OPENPROJECT_DEFAULT__LANGUAGE=en \
  openproject/openproject:17
```

For persistence (data survives restarts), add volume mounts:

```
textsudo mkdir -p /var/lib/openproject/{pgdata,assets}
docker run -d -p 8080:80 --name openproject \
  -e OPENPROJECT_HOST__NAME=localhost:8080 \
  -e SECRET_KEY_BASE=secret \
  -v /var/lib/openproject/pgdata:/var/openproject/pgdata \
  -v /var/lib/openproject/assets:/var/openproject/assets \
  openproject/openproject:17
```

Full docs at openproject.org/docs/installation-and-operations/installation/docker/ cover HTTPS, custom domains, and upgrades.

## Docker Compose Option

They also offer a `docker-compose.yml` in their repo for multi-container setups (separate DB, etc.). Pull with `docker compose up -d --build --pull always`.

This works seamlessly on Mac/Windows/WSL with Docker Desktop. Once running, enable the Timeline module for your draggable product roadmaps. Questions on config?

## How Excel Import Works

OpenProject provides a downloadable Excel template with VBA macros from their GitHub repo (github.com/opf/openproject_excel). You configure it with your instance's API key and project URL, then use it to:

- **Download** existing work packages to Excel for review/editing.
- **Upload/update** your Excel data (e.g., paste in features, tasks, descriptions, dates, assignees) back to OpenProject, creating or syncing artifacts with hierarchies (parent/child tasks).

Key steps:

- Download the template ZIP and open `OpenProjectAPI.xlsm`.
- Enable macros/content, enter your OpenProject URL/API token (from user settings), select project/query.
- Paste your data into columns like Subject, Description, Start/End Date, Type (task/milestone), Parent ID (for hierarchy).
- Hit Ctrl+B to sync—minimum columns: ID, Subject, Update status; add others like Assignee, Priority, Custom fields.

## Limitations and Tips

- Supports bi-directional sync for ongoing use, relations (e.g., "blocks 123"), custom fields (pre-create in OpenProject).
- Works with Community edition (no Enterprise needed); great for bulk-importing roadmaps from spreadsheets.
- No direct file upload in the web UI for Excel—use this tool or CSV/JSON via API for automation.