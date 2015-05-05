import json
import argparse
from repomanager import SyncRepo

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="")
args = parser.parse_args()

config_file = args.config
with open(config_file) as cf:
    data = json.load(cf)

for d in data:
    sync_repo = SyncRepo(data[d], name=d)
    print "name: " + sync_repo.name
    master_repo = sync_repo.run_sync()
