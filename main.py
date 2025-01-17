from pathlib import Path

from lib.api_client import Wrapper
from lib.database import Database

database_file = Path(__file__).parent / "sonarr.db"
config_file = Path(__file__).parent / "config.json"

sonarr = Wrapper(config_file)
db = Database(database_file)
rootfolder = sonarr.get_root()
quality = sonarr.get_qualities()

shows = db.get_shows()

for title, tvdbid in shows:
    print(f'{title} ({tvdbid})')
    if tvdbid is None or tvdbid == 0:
        print('   *** ERROR ***')
        continue
    r = sonarr.add_series(tvdbid)
    if r.status_code != 200:
        print(f'{r.status_code} {r.reason}: {r.text}')
