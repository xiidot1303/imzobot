import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(os.path.join('.env'))
WHERE = os.environ.get('WHERE')
TOKEN = os.environ.get('TOKEN')
BASEDIR = os.environ.get('BASEDIR')
if BASEDIR != "No":
    basedir = BASEDIR
else:
    basedir = os.path.dirname(os.path.abspath('__file__'))
