#!/bin/sh

# Trust the home directory
sh -c "git config --global --add safe.directory $PWD"

# Run the python application and pass the arguments
python /action/app.py $@
