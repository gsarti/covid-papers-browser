#!/bin/bash
# fill up db
./scripts/fill_db.sh
# and then start the web server :)
python ./scripts/run_api.py
