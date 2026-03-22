#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WeChat article helper for the local sync service.

This is the main entry point that delegates to the cli module.
The code has been split into multiple modules for better maintainability:
- api_client.py: HTTP request handling
- utils.py: Utility functions
- formatters.py: Output formatting
- commands.py: Command implementations
- cli.py: CLI argument parsing and main logic
"""

import sys
from pathlib import Path

# Add the scripts directory to the path for imports
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from cli import main

if __name__ == "__main__":
    raise SystemExit(main())
