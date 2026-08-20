"""
Django settings module loader.
Loads the appropriate settings file based on DJANGO_SETTINGS_MODULE environment variable.
"""

import os
from pathlib import Path

# Determine which settings file to use
env = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Import the appropriate settings module
if 'production' in env:
    from .production import *
elif 'staging' in env:
    from .staging import *
else:
    from .development import *
