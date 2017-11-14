from flask_socketio import SocketIO
from flask_mysql_util import MultiMySQL
from flask_mysql_util import MultiMySQL
from flask_authnz import FlaskAuthnz, MySQLRoles, UserGroups

from kafka import KafkaProducer
from kafka.errors import KafkaError
from config import SKIP_KAFKA_CONNECTION, KAFKA_BOOTSTRAP_SERVER
import json
import logging

logger = logging.getLogger(__name__)

__author__ = 'mshankar@slac.stanford.edu'

# Application context.
app = None

# Socket context
socketio = SocketIO()
# Set up connections to the databases
logbook_db = MultiMySQL(prefix="LOGBOOK")

# Set up the security manager
roles_db = MultiMySQL(prefix="ROLES")
security = FlaskAuthnz(MySQLRoles(roles_db, UserGroups()), "LogBook")

def __getKafkaProducer():
    if SKIP_KAFKA_CONNECTION:
        return None
    else:
        return KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

kafka_producer = __getKafkaProducer()
