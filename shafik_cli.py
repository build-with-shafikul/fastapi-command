import os
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# 🔥 AUTO VERSION (sync with setup.py manually once)
VERSION = "0.1.0"

app = typer.Typer(help="Shafikul CLI for FastAPI")
create_app_cli = typer.Typer(help="Create resources")
app.add_typer(create_app_cli, name="create")

console = Console()

# =========================================================
# 🎨 COLORED BANNER
# =========================================================
def show_banner():
    banner = Text("Shafikul CLI", style="bold cyan")
    subtitle = Text(f"Version {VERSION} • FastAPI Toolkit", style="green")
    panel = Panel.fit(
        f"{banner}\n{subtitle}",
        border_style="bright_blue",
    )
    console.print(panel)


# =========================================================
# 🚩 ROOT CALLBACK (--version)
# =========================================================
@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show CLI version",
        is_eager=True,
    ),
):
    if version:
        console.print(f"[bold green]Shafikul CLI v{VERSION}[/]")
        raise typer.Exit()


# =========================================================
# 📘 ABOUT COMMAND
# =========================================================
@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show CLI version",
        is_eager=True,
    ),
    about: bool = typer.Option(
        False,
        "--about",
        help="Show information about Shafikul CLI",
        is_eager=True,
    ),
):
    if version:
        console.print(f"[bold green]Shafikul CLI v{VERSION}[/]")
        raise typer.Exit()

    if about:
        show_banner()
        console.print("\n[bold]Author:[/] Shafikul Islam")
        console.print("[bold]Purpose:[/] FastAPI project scaffolding")
        console.print("[bold]GitHub:[/] https://github.com/yourname/shafikul-cli")
        console.print("[bold]License:[/] MIT\n")
        raise typer.Exit()

# =========================================================
# 📁 FILE GENERATOR
# =========================================================
def create_file_structure(dir_name: str, file_name: str, content: str = ""):
    os.makedirs(dir_name, exist_ok=True)

    init_path = os.path.join(dir_name, "__init__.py")
    if not os.path.exists(init_path):
        Path(init_path).touch()
        console.print(f"[cyan]Created:[/] {init_path}")

    file_path = os.path.join(dir_name, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(content)
        console.print(f"[green]Created:[/] {file_path}")
    else:
        console.print(f"[yellow]Already exists:[/] {file_path}")


# =========================================================
# 🛠 CREATE APP
# =========================================================
@create_app_cli.command("app")
def create_app(
    target: Optional[str] = typer.Argument(None, help="router, models, or database")
):
    show_banner()

    if target is None:
        console.print("\n[bold cyan]Options:[/] router, models, database")
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
        console.print("[red]Unknown target![/]")


if __name__ == "__main__":
    app()