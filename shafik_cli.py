import os
import typer
import sys 
import subprocess
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

def create_html_file(file_name: str, content: str):
    """
    Create or update an HTML file dynamically.
    
    Args:
        file_name (str): Name of the file to create (e.g., 'index.html')
        content (str): HTML content to write into the file
    """
    # template folder path
    templates_dir = Path("templates")  # root relative path
    target_file = templates_dir / file_name

    # ✅ Create templates folder if missing
    if not templates_dir.exists():
        templates_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[cyan]Created folder:[/] {templates_dir}")
    else:
        console.print(f"[yellow]Folder already exists:[/] {templates_dir}")

    # ✅ Create or update the HTML file
    if not target_file.exists():
        target_file.touch()
        console.print(f"[cyan]Created file:[/] {target_file}")
    else:
        console.print(f"[yellow]File already exists, updating:[/] {target_file}")

    # Write the HTML content
    target_file.write_text(content, encoding="utf-8")
    console.print(f"[green]HTML content written successfully to {target_file}![/]")


# =========================================================
# env generator
# =========================================================
def ensure_env_file():
    env_file = ".env"

    required_vars = {
        "DATABASE_URL": "postgresql://user:password@localhost:5432/dbname",
        "SSL_PATH": "./certs/ca.pem",
    }

    # ❌ File doesn't exist → create full
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("# Database config\n")
            for key, value in required_vars.items():
                f.write(f"{key}={value}\n")
        console.print("[green]Created .env file[/]")
        return

    # ✅ File exists → read current vars
    with open(env_file, "r") as f:
        lines = f.readlines()

    existing_keys = set()
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            existing_keys.add(line.split("=")[0].strip())

    # find missing vars
    missing = {
        k: v for k, v in required_vars.items() if k not in existing_keys
    }

    if not missing:
        console.print("[yellow].env already up-to-date[/]")
        return

    # append missing vars
    with open(env_file, "a") as f:
        f.write("\n# Added by Shafikul CLI\n")
        for key, value in missing.items():
            f.write(f"{key}={value}\n")

    console.print("[cyan]Updated .env with missing variables[/]")

#=========================================================
# check main.py file a code add 
#=========================================================
def ensure_main_py():
    main_file = "main.py"

    new_code = """from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path
from router import users

app = FastAPI()

# =================================
# Add Middleware
# =================================
app.middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "http://localhost:8000", "http://127.0.0.1:8000"]
)

# =================================
# Include Router
# =================================
app.include_router(users.router)

# =================================
# Template Dir & Static Dir
# =================================
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# =================================
# 404 Route 
# =================================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"error": "Resource Not Found", "details": exc.detail}
        )
        # return template.TemplateResponse(
        #     '404.html',
        #     {'request': request},
        #     status_code=404
        # )
    return JSONResponse(
         status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# =================================
# Route Start ... 
# =================================
@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": Request}
    )

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

def ensure_db_in_main():
    main_file = "main.py"

    import_block = """from fastapi import Depends
from sqlalchemy.orm import Session
from app import database

"""

    db_block = """def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db: Session = Depends(get_db)

"""

    # ❌ main.py নেই → create minimal
    if not os.path.exists(main_file):
        with open(main_file, "w") as f:
            f.write(import_block + db_block)
        console.print("[green]Created main.py with DB dependency[/]")
        return

    with open(main_file, "r") as f:
        existing = f.read()

    updated = existing

    # add import if missing
    if "from app import database" not in existing:
        updated = import_block + updated
        console.print("[cyan]Added DB imports to main.py[/]")

    # add get_db if missing
    if "def get_db()" not in existing:
        updated = updated + "\n\n" + db_block
        console.print("[cyan]Added get_db() to main.py[/]")

    # write back only if changed
    if updated != existing:
        with open(main_file, "w") as f:
            f.write(updated)
    else:
        console.print("[yellow]main.py already has DB setup[/]")


# =========================================================
# 🌐 package install for dependicy
# =========================================================
def install_dependencies(packages: list[str]):
    console.print("[cyan]🌐 Installing dependencies...[/]")
    for pkg in packages:
        subprocess.call([sys.executable, "-m", "pip", "install", pkg])

# =========================================================
# 🛠 CREATE APP
# =========================================================
@create_app_cli.command("app")
def create_app(
    target: Optional[str] = typer.Argument(None, help="router, models, database, or html")
):
    show_banner()
   
    if target is None:
        console.print("\n[bold cyan]Options:[/] \n 1: router \n 2: models \n 3: html \n 4: database")
        target = typer.prompt("What do you want to create?")

    # normalize input
    target = str(target).strip().lower()

    # map numeric input to text
    num_map = {
        "1": "router",
        "2": "models",
        "3": "html",
        "4": "database"
    }

    if target in num_map:
        target = num_map[target]

    if target == "router":
        content = """from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

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

        # ✅ NEW: inject DB into main.py
        ensure_db_in_main()

        # ✅ Create .env
        ensure_env_file()

        # ✅ Auto install deps
        install_dependencies([
            "fastapi",
            "uvicorn[standard]",
            "jinja2",
            "sqlalchemy",
            "python-dotenv"
        ])

       
        console.print(
    Panel(
        "[bold underline cyan]alembic init migrations[/]",
        title="🚀 Run This Command",
        border_style="green"
    ),
    Panel(
        "[bold underline cyan]alembic revision --autogenerate -m 'create users table'[/]",
        title="🚀 Run This Command",
        border_style="green"
    ),
    Panel(
        "[bold underline cyan]uvicorn main:app --reload[/]",
        title="🌐 Running Server",
        border_style="green"
    )
)

    elif target == "html":
        file_name = typer.prompt("Enter file name default", default="index.html").strip()
        if file_name == 'index.html':
            file_content = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shafikul FastAPI App</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        // Tailwind config for custom transitions or dark mode
        tailwind.config = {
            darkMode: 'class',
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
</head>

<body class="bg-slate-100 dark:bg-slate-950 transition-colors duration-500">

    <div class="fixed inset-0 -z-10 overflow-hidden">
        <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-purple-500/30 rounded-full blur-[120px] animate-pulse"></div>
        <div class="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-blue-500/30 rounded-full blur-[120px]"></div>
    </div>

    <!-- Main Container -->
    <div class="min-h-screen flex flex-col items-center justify-center p-6">
        
        <!-- Dark Mode Toggle -->
        <button onclick="document.documentElement.classList.toggle('dark')" class="absolute top-5 right-5 p-2 bg-white/20 dark:bg-gray-800/30 backdrop-blur-md border border-white/20 dark:border-white/10 rounded-full shadow-lg hover:scale-110 transition-transform">
            <span class="dark:hidden">🌙</span>
            <span class="hidden dark:inline">☀️</span>
        </button>

        <!-- Card -->
        <div class="w-full max-w-md p-8 md:p-10 rounded-3xl
                    bg-white/30 dark:bg-white/5 
                    backdrop-blur-xl backdrop-saturate-150
                    border border-white/40 dark:border-white/10
                    shadow-[0_8px_32px_0_rgba(31,38,135,0.2)]
                    text-center transform transition-all hover:shadow-2xl">
            
            <!-- Icon And Logo -->
            <div class="inline-flex p-3 rounded-2xl bg-indigo-500/20 mb-6">
                <svg class="w-10 h-10 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
            </div>

            <h1 class="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-300 dark:to-purple-300 bg-clip-text text-transparent mb-4">
                Shafikul FastAPI
            </h1>
            
            <p class="text-slate-600 dark:text-slate-300 mb-8 leading-relaxed">
                Build blazing fast APIs with the power of Python and modern UI design. High performance, easy to code, ready for production.
            </p>

            <div class="space-y-4">
                <a href="#" class="block w-full py-3 px-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow-lg shadow-indigo-500/30 transition-all hover:-translate-y-1">
                    Get Started
                </a>
                
                <a href="#" class="block w-full py-3 px-6 bg-white/50 dark:bg-white/10 hover:bg-white/80 dark:hover:bg-white/20 text-slate-800 dark:text-white font-semibold rounded-xl border border-white/20 transition-all">
                    Documentation
                </a>
            </div>

            <!-- Status -->
            <div class="mt-8 flex justify-center gap-4">
                <div class="flex items-center gap-2 px-3 py-1 bg-green-500/20 rounded-full">
                    <span class="w-2 h-2 bg-green-500 rounded-full animate-ping"></span>
                    <span class="text-xs font-medium text-green-700 dark:text-green-400">API Live</span>
                </div>
                <div class="flex items-center gap-2 px-3 py-1 bg-blue-500/20 rounded-full text-blue-700 dark:text-blue-400">
                    <span class="text-xs font-medium italic underline">v1.0.0</span>
                </div>
            </div>
        </div>

        <p class="mt-8 text-slate-500 dark:text-slate-500 text-sm">
            © 2024 Shafikul. Made with ❤️
        </p>
    </div>

</body>
</html>
"""
        else:
            file_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shafikul FastAPI APP</title>
</head>
<body>
    <h1>Hello User</h1>
</body>
</html>
"""
        create_html_file(file_name, file_content)

    else:
        console.print("[red]Unknown target![/]")


if __name__ == "__main__":
    app()