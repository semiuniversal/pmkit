# pmkit

Product Management Toolkit wrapping OpenProject.

## Usage

1. Create a `.env` file from `.env.example`.
2. Run `pmkit up` to start the stack.
3. Access OpenProject at `http://localhost:8080` (or configured port).
4. Login with default credentials: `admin` / `admin`. You will be asked to change the password on first login.

## Excel Integration & API Access

`pmkit` includes tools to import/export work packages to Excel. This requires an API Key from your **local** OpenProject instance (no external account needed).

1.  Log in to your local instance (e.g., `http://localhost:8080`).
2.  Click your user avatar (top right) -> **My Account**.
3.  Select **Access Tokens** from the sidebar.
4.  Click **generate** in the **API** row.
5.  Use this key with the CLI:
    ```bash
    # Export
    uv run pmkit excel export --project <project-id> --apikey <your-key>

    # Import
    uv run pmkit excel imports --project <project-id> --input work_packages.xlsx
    ```
    *Tip: You can also set `OPENPROJECT_API_KEY` in your `.env` file to avoid typing it.*
