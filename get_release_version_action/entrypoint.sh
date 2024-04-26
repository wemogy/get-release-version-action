#!/bin/sh

# Trust the home directory
sh -c "git config --global --add safe.directory $PWD"

# Run the python application and pass the arguments
poetry run -C /action python /action/get_release_version_action/app.py "$@"
