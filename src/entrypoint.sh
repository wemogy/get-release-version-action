#!/bin/sh

# Trust the home directory
sh -c "git config --global --add safe.directory $PWD"

# Run the python application and pass the arguments
cd /action/get_release_version_action
poetry run python app.py $@
