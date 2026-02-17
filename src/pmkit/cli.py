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
    
    cmd = ["docker", "compose", "up"]
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
    try:
        subprocess.check_call(["docker", "compose", "down"])
        click.echo("Stack stopped successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error stopping stack: {e}", err=True)
        exit(1)

@main.command()
def logs():
    """View logs from the stack."""
    try:
        subprocess.check_call(["docker", "compose", "logs", "-f"])
    except subprocess.CalledProcessError as e:
        click.echo(f"Error viewing logs: {e}", err=True)
        exit(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
