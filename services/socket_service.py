import logging
import json
import requests
from threading import Thread

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from flask_socketio import emit, join_room
from context import socketio, security
from flask import Blueprint, jsonify, request
from config import SKIP_KAFKA_CONNECTION, KAFKA_BOOTSTRAP_SERVER, SERVER_IP_PORT


'''
The socket endpoint for web services. 
We have "rooms" for experiments; the client's join the rooms for updates.
The server side intercepts Kafka messages and posts these back to the client. 
In addition, one can send custom messages back to the client by POSTing to the send_message_to_client.
'''

__author__ = 'jacob.defilippis@cosylab.com'
socket_service_blueprint = Blueprint('socket_service_api', __name__)

logger = logging.getLogger(__name__)


class Manager(object):
    clients = 0
manager = Manager()


@socketio.on('connect', namespace='/psdm_ws')
def connect():
    """
    New client connects to the socket.
    """
    manager.clients += 1

@socketio.on('join', namespace='/psdm_ws')
def on_join(experiment_name):
    if security.__check_privilege_for_experiment('read', experiment_name):
        logger.info("User %s joined socketio room for experiment %s" % (security.get_current_user_id(), experiment_name))
        join_room(experiment_name)
    else:
        logger.warn("User %s does not have permission for socketio room for experiment %s" % (security.get_current_user_id(), experiment_name))
        join_room("Noop")

@socketio.on('disconnect', namespace='/psdm_ws')
def disconnect():
    """
    Client disconnects from socket.
    :return:
    """
    manager.clients -= 1




@socket_service_blueprint.route("/send_message_to_client/<experiment_name>/<message_type>", methods=["POST"])
def sock_send_message_to_client(experiment_name, message_type):
    """
    Send the message to all clients connected to this experiment's room
    :param: experiment_name - The experiment_name; for example, diadaq13 
    :param: message_type - The message type/business object type of the message; for example, elog
    """
    # Push update only if some clients are connected.
    if manager.clients > 0:
        socketio.emit(message_type, request.json, namespace='/psdm_ws' , room=experiment_name)

    return jsonify(success=True)


# Subscribe to Kafka messages for these topics and send them across to the client.
def kafka_2_websocket(topics):
    """
    Subscribe to a list of topics from Kafka. 
    Route messages on these topics to the web socket clients.
    """
    def subscribe_kafka():
        if SKIP_KAFKA_CONNECTION:
            logger.warn("Skipping Kafka connection")
            return
        consumer = KafkaConsumer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER])
        consumer.subscribe(topics)
    
        for msg in consumer:
            logger.info("Message from Kafka %s", msg)
            info = json.loads(msg.value)
            logger.info("JSON from Kafka %s", info)
            message_type = msg.topic
            exp_name = info['exper_name']
            requests.post("http://" + SERVER_IP_PORT + "/ws/socket/send_message_to_client/" + exp_name + "/" + message_type, json=info)
                
    
    # Create thread for kafka consumer
    kafka_client_thread = Thread(target=subscribe_kafka)
    kafka_client_thread.start()
