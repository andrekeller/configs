#!/usr/bin/env python3
"""
confi.gs management utility
"""
# stdlib
import os
import sys
# django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")
    execute_from_command_line(sys.argv)
