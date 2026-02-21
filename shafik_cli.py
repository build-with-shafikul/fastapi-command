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


def ensure_main_py():
    main_file = "main.py"

    new_code = """from fastapi import FastAPI
from sqlalchemy.orm import Session
from router import users

app = FastAPI()
app.include_router(users.router)

"""

    # ❌ main.py নেই → create
    if not os.path.exists(main_file):
        with open(main_file, "w") as f:
            f.write(new_code)
        console.print("[green]Created main.py with FastAPI setup[/]")
        return

    # ✅ আছে → read existing content
    with open(main_file, "r") as f:
        existing = f.read()

    # duplicate check
    if "app = FastAPI()" in existing:
        console.print("[yellow]main.py already configured[/]")
        return

    # prepend new code
    with open(main_file, "w") as f:
        f.write(new_code + existing)

    console.print("[cyan]Updated main.py (prepended FastAPI setup)[/]")

    
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

        # ✅ NEW: ensure main.py exists and configured
        ensure_main_py()

    elif target == "models":
        content = """from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(250), nullable=True)
    
# add more table
"""
        create_file_structure("app", "models.py", content)

    elif target == "database":
        content = """import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={
        "ssl": {
            "ca": os.getenv("SSL_PATH") 
        }
    },
    pool_pre_ping=True,    
    pool_recycle=300, 
    pool_size=5,      
    max_overflow=10    

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
"""
        create_file_structure("app", "database.py", content)

    else:
        console.print("[red]Unknown target![/]")


if __name__ == "__main__":
    app()