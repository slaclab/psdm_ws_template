from flask_socketio import SocketIO
from flask_mysql_util import MultiMySQL
#from psdmauth.auth_client_flask import FlaskSecurityClient
#from psdmauth.auth_server_dal_db import DatabaseDal

__author__ = 'mshankar@slac.stanford.edu'

# Application context.
app = None

# Socket context
socketio = SocketIO()
# Set up connections to the databases
logbook_db = MultiMySQL(prefix="LOGBOOK")
roles_db = MultiMySQL(prefix="ROLES")

# Set up the security manager
#security = FlaskSecurityClient(DatabaseDal(roles_db), "LogBook")
