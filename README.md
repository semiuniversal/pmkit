# pmkit

Product Management Toolkit wrapping OpenProject.

## Usage

## Usage

1. Create a `.env` file from `.env.example`.
2. Run `pmkit up` to start the stack.
3. Access OpenProject at `http://localhost:8080`.
4. Login with default credentials: `admin` / `admin`. You will be asked to change the password on first login.

*Note: If you are using **Podman** on Windows/Mac:*
1.  Ensure `podman` and `podman-compose` are installed on your host system.
2.  If running from WSL, you may need to alias `podman` to `podman.exe` or configure the WSL-Podman bridge.
3.  The simplest test is to run `podman-compose up -d` from a PowerShell terminal in this directory.

## Excel Integration & API Access

`pmkit` includes tools to import/export work packages to Excel. This requires an API Key.

1.  Log in to your instance.
2.  Click your user avatar (top right) -> **My Account**.
3.  Select **Access Tokens** from the sidebar.
4.  Click **generate** in the **API** row.
5.  Use this key with the CLI:
    ```bash
    # Export
    pmkit excel export --project <project-id> --apikey <your-key>

    # Import
    pmkit excel imports --project <project-id> --input work_packages.xlsx
    ```
    *Tip: You can also set `OPENPROJECT_API_KEY` in your `.env` file.*
