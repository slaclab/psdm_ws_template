# psdm-ws-template

This repo contains a template app for PSDM web services; use this repo as the basis for any new application.
This repo demonstrates the integration of these tools
- Python 3
- Flask
- Conda
- SocketIO
- Kafka
- PSDM modules like flask_authnz/flask_mysql_util etc
- Mongo/MySQL.

The rest of this document serves as user guide on how to combine these tools to generate PSDM web services and applications.

### Files and Folders
Even the simplest application consists of multiple files organized into multiple folders.
We could have put all of this in a couple of files but this makes developing applications of any reasonable size difficult.
First the folders
- `dal` - This folder contains the data access layer/business object layer.
- `runscripts` - This folder contains the startup scripts for the application.
- `services` - This folder contains the Flask web service endpoints for the application.
- `static` - This folder contains the application specific Javascript and CSS files.
- `templates` - This folder contains the HTML templates for the UI for the application.

Now the files
- `dal/business_object.py` - Place all of your business logic in files in the `dal`. For example, the business logic for the `elog` belongs in `dal/elog.py`. The business logic methods typically
  - Take strings, ints and other attribute types as inputs
  - Return strings, ints and other JSON'able objects as outputs
  - Deal solely with reading/writing data from the database.
  - Contain all of the business logic of the application and none of the plumbing.
- `dal/sql_queries.py` - Consolidate all of your Mongo/SQL queries into a separate file in the `dal`.
- `services/business_service.py` - Place all of your Flask web service endpoints in files in the `services` folder. For example, the web service endpoints for the `elog` belong in `services/elog_service.py`. The web service endpoints typically contain
  - All of the plumbing for your application.
  - This is where web service parameters are unpacked from HTTP/JSON and data is sent back to the browser as JSON.
  - This is also where messages are published into Kakfa. The socket service endpoint automatically pushes Kafka messages to the browser.
  - This is also where authentication and authorization are enforced using `authentication_required` and `authorization_required` decorators. The order of the decorators is important. For example, to support a web service endpoint for getting `elog` entries for an experiment, use code that looks like so.
  ```
  @business_service_blueprint.route("/<experiment_name>/elog", methods=["GET"])
  @context.security.authentication_required
  @context.security.authorization_required("read")
  def svc_get_elog_for_experiment(experiment_name):
  ```
  With this endpoint, the web service URL `http://localhost/psdm/ws/business/diadaq13/elog` will be satisfied by the method `svc_get_elog_for_experiment` for the experiment `diadaq13` for those users who have the `read` privilege for this experiment. Similarly, the
  ```
  @business_service_blueprint.route("/<experiment_name>/elog", methods=["POST"])
  @context.security.authentication_required
  @context.security.authorization_required("post")
  def svc_add_elog_for_experiment(experiment_name):
  ```
  endpoint allows the following command
  ```
  curl -XPOST "http://localhost/psdm/ws/business/diadaq13/elog"
       -H 'Content-Type: application/json' -d'
       {
         "content" : "Posting a sample elog entry from the command line",
         "content_type": "TEXT",
         "run_num": 8
      }'
  ```
  to `POST` an entry into the elog for those users who have the `post` privilege for this experiment.
- For each HTML page in your application (for example, http://localhost/psdm/diadaq13/elog), create these files
  - `templates/elog.html` - This contains the JINJA2 template for your HTML page.
    - Use relative paths for all Javascript and CSS files. Your application may be deployed at a different location in the webserver namespace.
    - Use `../js` for Javascript library files. For example, include JQuery like so
    ```
    <script type="text/javascript" src="../js/jquery/jquery.min.js"></script>
    ```
    We'll later create a hook that will serve Javascript library files straight from the conda environment.
    - Include the page specific Javascript and CSS files like so
    ```
    <link rel=stylesheet type=text/css href="../static/elog.css">
    <script type="text/javascript" src="../static/elog.js"></script>
    ```
    - Your web page will make use of backend web services and other information. Declare them in the template like so
    ```
      <script type="text/javascript">
  		  var elog_for_experiment_url = "{{ '../ws/business/' + experiment_name + '/elog' }}";
      	var experiment_name = "{{ experiment_name }}";
      </script>
    ```
    - Use Bootstrap to create fluid containers and responsive tables.
    - Create elements with id's for containers of dynamic information. For example, if you are intending to make a web service all to update a HTML table, add an id to the table.
    - Most of the UI logic will be in the page specific Javascript. At a very high level
      - Create one or more Mustache templates
      - Make backend web service calls to the web service endpoints.
      - Convert the JSON to HTML using the Mustache templates.
      - Insert the HTML into the page using the id's defined for the container elements.
      - The socket service publishes Kafka messages into the document. Subscribe and process using something like so
      ```
      $(document).on('elog', function(event, elogData) {
        if ('CRUD' in elogData && elogData['CRUD'] == 'INSERT') {
            var single_elog_item =  Mustache.render(elog_template, elogData);
            $("#elogs").prepend(single_elog_item);
        }   
      });
      ```
- `context.py` - Database connections, Kafka connectors, security objects and other application wide singletons are created as module variables in the context.
- `pages.py` - In addition to Flask blueprints for your HTML pages, a hook to serve Javascript library files straight from the conda environment is also registered here.
```
@pages_blueprint.route('/js/<path:path>')
def send_js(path):
    # Serve files directly from $CONDA_PREFIX/lib/node_modules.
```
- `start.py` - This file creates the Flask app for your application and bring together the various pieces using `register_blueprint` and `init_app`. This is the starting point for the application and will be passed to `gunicorn` in the `runscripts`. This is also where we initialize the websocket service.
- `runscripts/rundev.sh` - The startup script for the application.
  - Set environment variables using commands like so `export SERVER_IP_PORT="0.0.0.0:5000"`
  - Pick up database passwords etc by sourcing files external to the application - `EXTERNAL_CONFIG_FILE`
  - Use `gunicorn` to start the application like so
  ```
  exec gunicorn start:app -b ${SERVER_IP_PORT} --worker-class eventlet --reload \
         --log-level=DEBUG --env DEBUG=TRUE --capture-output --enable-stdio-inheritance \
         --access-logfile - --access-logformat "${ACCESS_LOG_FORMAT}"
  ```
    - The `exec` is needed for `supervisord`. Without it, `supervisord` cannot properly detect the application process.
    - Use a recent version of `gunicorn` that supports `--capture-output --enable-stdio-inheritance`. This should send all of the application output into `supervisord`s logs and is critical for debugging the application.

### Logging
In your python files, use the following for logging
```
import logging
logger = logging.getLogger(__name__)
logger.info("Making change to experiment -  %s", experiment_name)
```
In your Javascript files, use `console.log` for debug logging. To notify the user that something worked/did not work, use `noty`. For example,
```
noty( { text: errmsg, layout: "topRight", type: "error" } );
```

