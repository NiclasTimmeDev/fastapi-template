# -------------------------------------------------------------------------------
# Bootstrap CLI application.
# Config and methods are located in the app.core.cli
# This file right here only exists to make accessing the cli tool easier by
# not having to prefix the executed script with /app/core/cli.
# -------------------------------------------------------------------------------
from app.core.cli import main
main.start()
