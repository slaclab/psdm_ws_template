from flask_socketio import SocketIO
from flask_mysql_util import MultiMySQL
from flask_mysql_util import MultiMySQL
from flask_authnz import FlaskAuthnz, MySQLRoles, UserGroups

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
