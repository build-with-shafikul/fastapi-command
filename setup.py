from setuptools import setup

VERSION = "0.1"

setup(
    name="shafikul-cli",
    version=VERSION,
    py_modules=["shafik_cli"], 
    install_requires=[
        "typer", "rich",
    ],
    entry_points={
        "console_scripts": [
            "shafikul=shafik_cli:app",
        ],
    },
)