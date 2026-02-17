import os
import subprocess
import click
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@click.group()
def main():
    """PMKit: Product Management Toolkit wrapping OpenProject."""
    pass

def get_compose_cmd():
    """Detect the appropriate compose command."""
    # Allow override
    if os.getenv("PMKIT_COMPOSE_CMD"):
        return os.getenv("PMKIT_COMPOSE_CMD").split()

    import shutil
    if shutil.which("podman-compose"):
        return ["podman-compose"]
    elif shutil.which("podman"):
        return ["podman", "compose"]
    else:
        return ["docker", "compose"]

@main.command()
@click.option('--detach', '-d', is_flag=True, default=True, help="Run containers in the background")
def up(detach):
    """Start the OpenProject stack."""
    # Ensure .env exists
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        click.echo("⚠️  No .env file found. Generating one from .env.example...")
        example_path = os.path.join(os.getcwd(), ".env.example")
        
        if os.path.exists(example_path):
            import secrets
            with open(example_path, "r") as f:
                content = f.read()
            
            # Generate secure secret
            secure_key = secrets.token_urlsafe(32)
            content = content.replace("change_me_in_production_to_a_long_random_string", secure_key)
            
            with open(env_path, "w") as f:
                f.write(content)
            click.echo(f"✅ Created .env with generated secret key.")
            
            # Reload env vars
            load_dotenv(override=True)
        else:
             click.echo("❌ .env.example not found. Cannot generate .env.", err=True)

    click.echo("Starting OpenProject stack...")
    
    # Ensure data directories exist
    data_dir = os.getenv("DATA_DIR", "./data")
    os.makedirs(os.path.join(data_dir, "pgdata"), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "assets"), exist_ok=True)
    
    cmd_base = get_compose_cmd()
    click.echo(f"Using compose command: {' '.join(cmd_base)}")
    
    cmd = cmd_base + ["up"]
    if detach:
        cmd.append("-d")
        
    try:
        subprocess.check_call(cmd)
        click.echo("Stack started successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error starting stack: {e}", err=True)
        exit(1)

@main.command()
def down():
    """Stop the OpenProject stack."""
    click.echo("Stopping OpenProject stack...")
    cmd_base = get_compose_cmd()
    
    try:
        subprocess.check_call(cmd_base + ["down"])
        click.echo("Stack stopped successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error stopping stack: {e}", err=True)
        exit(1)

@main.command()
def logs():
    """View logs from the stack."""
    cmd_base = get_compose_cmd()
    try:
        subprocess.check_call(cmd_base + ["logs", "-f"])
    except subprocess.CalledProcessError as e:
        click.echo(f"Error viewing logs: {e}", err=True)
        exit(1)
    except KeyboardInterrupt:
        pass

@main.group()
def excel():
    """Excel import/export commands."""
    pass

@excel.command()
@click.option('--project', '-p', prompt=True, help="Project identifier (e.g. 'demo-project')")
@click.option('--output', '-o', default='work_packages.xlsx', help="Output file path")
@click.option('--apikey', envvar='OPENPROJECT_API_KEY', prompt=True, hide_input=True, help="OpenProject API Key")
def export(project, output, apikey):
    """Export work packages to Excel."""
    from .excel import export_work_packages
    export_work_packages(output, project, apikey)

@excel.command()
@click.option('--project', '-p', prompt=True, help="Project identifier (e.g. 'demo-project')")
@click.option('--input', '-i', default='work_packages.xlsx', help="Input file path")
@click.option('--apikey', envvar='OPENPROJECT_API_KEY', prompt=True, hide_input=True, help="OpenProject API Key")
def imports(project, input, apikey):
    """Import work packages from Excel."""
    from .excel import import_work_packages
    import_work_packages(input, project, apikey)

if __name__ == "__main__":
    main()
