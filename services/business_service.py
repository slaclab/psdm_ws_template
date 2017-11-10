'''
Code for the business logic.
Here's where you do the actual business logic using functions from the dal's business object.
The public methods here are expected to be Flask blueprint endpoints.
We get the arguments for the business logic from Flask; make various calls to the dal's and then send JSON responses.
Events are published into Kafka and the Websocket layer here.
Use security's authentication_required and authorization_required decorators to enforce authz/authn.

'''

import os
import json

import requests
import context

from kafka import KafkaProducer
from kafka.errors import KafkaError

from flask import Blueprint, jsonify, request, url_for, Response
    
from dal.business_object import get_experiments_for_instrument

__author__ = 'mshankar@slac.stanford.edu'

business_service_blueprint = Blueprint('business_service_api', __name__)

#kafka_producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER], value_serializer=lambda m: json.dumps(m).encode('ascii'))

@business_service_blueprint.route("/<instrument_name>/experiments", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def svc_get_experiments_for_instrument(instrument_name):
    """
    Get the experiments for an instrument
    :param instrument_id: Id of the instrument.
    :return: JSON of the experiment infos for the experiment
    """
    experiments = get_experiments_for_instrument(instrument_name)

    return jsonify({'success': True, 'value': experiments})

