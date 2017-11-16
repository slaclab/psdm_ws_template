import json
import logging
import os

from flask_mysql_util import MultiMySQL
from flask_mysql_util import MultiMySQL
from flask_authnz import FlaskAuthnz, MySQLRoles, UserGroups

from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)

__author__ = 'mshankar@slac.stanford.edu'

# Application context.
app = None

# Set up connections to the databases
logbook_db = MultiMySQL(prefix="LOGBOOK")

# Set up the security manager
roles_db = MultiMySQL(prefix="ROLES")
security = FlaskAuthnz(MySQLRoles(roles_db, UserGroups()), "LogBook")

def __getKafkaProducer():
    if os.environ.get("SKIP_KAFKA_CONNECTION", False):
        return None
    else:
        return KafkaProducer(bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP_SERVER", "localhost:9092")], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

kafka_producer = __getKafkaProducer()
