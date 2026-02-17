import os
import click
import requests
import pandas as pd
from typing import Optional

def get_api_session(api_key: str):
    session = requests.Session()
    session.auth = ('apikey', api_key)
    return session

def get_base_url():
    host = os.getenv("OPENPROJECT_HOST_NAME", "localhost:8080")
    protocol = "https" if os.getenv("OPENPROJECT_HTTPS", "false").lower() == "true" else "http"
    return f"{protocol}://{host}"

def export_work_packages(output_file: str, project_identifier: str, api_key: str):
    """Fetch work packages and save to Excel."""
    base_url = get_base_url()
    session = get_api_session(api_key)
    
    # Simple fetch of all WPs
    # In a real scenario, handling pagination is needed.
    # We'll fetch the first 100 for this MVP.
    url = f"{base_url}/api/v3/projects/{project_identifier}/work_packages?pageSize=100"
    
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        click.echo(f"Error connecting to OpenProject: {e}", err=True)
        # If 404, maybe project doesn't exist
        if e.response and e.response.status_code == 404:
             click.echo(f"Project '{project_identifier}' not found.", err=True)
        return

    wps = []
    embedded = data.get("_embedded", {})
    elements = embedded.get("elements", [])
    
    for element in elements:
        wp = {
            "ID": element.get("id"),
            "Subject": element.get("subject"),
            "Description": element.get("description", {}).get("raw", ""),
            "Type": element.get("_links", {}).get("type", {}).get("title"),
            "Status": element.get("_links", {}).get("status", {}).get("title"),
            "Priority": element.get("_links", {}).get("priority", {}).get("title"),
            "Start Date": element.get("startDate"),
            "Due Date": element.get("dueDate"),
            "Lock Version": element.get("lockVersion")
        }
        wps.append(wp)

    if not wps:
        click.echo("No work packages found.")
        # Create an empty dataframe with columns for template purposes
        df = pd.DataFrame(columns=["ID", "Subject", "Description", "Type", "Status", "Priority", "Start Date", "Due Date", "Lock Version"])
    else:
        df = pd.DataFrame(wps)
    
    df.to_excel(output_file, index=False)
    click.echo(f"Exported {len(wps)} work packages to {output_file}")

def import_work_packages(input_file: str, project_identifier: str, api_key: str):
    """Read Excel and create/update work packages."""
    # This is a scaffolding placeholder. 
    # Real implementation needs to handle ID mapping for updates vs creates.
    # For MVP, we will only log what we would do.
    
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
         click.echo(f"Error reading Excel file: {e}", err=True)
         return

    base_url = get_base_url()
    session = get_api_session(api_key)
    
    click.echo(f"Processing {len(df)} rows from {input_file}...")
    
    for index, row in df.iterrows():
        wp_id = row.get("ID")
        subject = row.get("Subject")
        
        if pd.isna(wp_id):
            click.echo(f"Row {index}: Creating new WP '{subject}' (Not Implemented in MVP)")
            # POST /api/v3/projects/{id}/work_packages
        else:
             click.echo(f"Row {index}: Updating WP {wp_id} '{subject}' (Not Implemented in MVP)")
             # PATCH /api/v3/work_packages/{id}
