import os
import json
from collections import OrderedDict

__author__ = 'mshankar@slac.stanford.edu'


# Use environment variables for configuration. 
# The name of the environment variable is the same as the name of the variable in the config object
SKIP_KAFKA_CONNECTION=bool(os.environ.get("SKIP_KAFKA_CONNECTION", False))
KAFKA_BOOTSTRAP_SERVER=os.environ.get("KAFKA_BOOTSTRAP_SERVER", "localhost:9092")
