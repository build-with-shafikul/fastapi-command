VERSION = "0.1"

import os
import typer
from pathlib import Path
from typing import Optional


app = typer.Typer(help="Shafikul CLI for FastAPI")
create_app_cli = typer.Typer(help="Create resources")

app.add_typer(create_app_cli, name="create")

@app.command()
def version():
    typer.echo(f"Shafikul CLI v{VERSION}")
    

def create_file_structure(dir_name: str, file_name: str, content: str = ""):
    os.makedirs(dir_name, exist_ok=True)

    init_path = os.path.join(dir_name, "__init__.py")
    if not os.path.exists(init_path):
        Path(init_path).touch()
        typer.echo(f"Created: {init_path}")

    file_path = os.path.join(dir_name, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(content)
        typer.echo(f"Created: {file_path}")
    else:
        typer.secho(f"{file_path} already exists!", fg=typer.colors.YELLOW)


@create_app_cli.command("app")
def create_app(
    target: Optional[str] = typer.Argument(None, help="router, models, or database")
):
    if target is None:
        typer.echo("Options: router, models, database")
        target = typer.prompt("What do you want to create?")

    target = target.lower()

    if target == "router":
        content = """from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def index():
    return {"message": "Router working"}
"""
        create_file_structure("router", "users.py", content)

    elif target == "models":
        content = """from .database import Base
from sqlalchemy import Column, Integer

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
"""
        create_file_structure("app", "models.py", content)

    elif target == "database":
        content = """from sqlalchemy import create_engine
# Database connection logic here
"""
        create_file_structure("app", "database.py", content)

    else:
        typer.secho("Unknown target!", fg=typer.colors.RED)


if __name__ == "__main__":
    app()