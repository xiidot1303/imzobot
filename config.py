import os
from dotenv import load_dotenv
from pathlib import Path
basedir = os.path.dirname(os.path.abspath('files'))
load_dotenv(os.path.join('.env'))
WHERE = os.environ.get('WHERE')
TOKEN = os.environ.get('TOKEN')

