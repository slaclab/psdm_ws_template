'''
The model level business logic goes here.
Most of the code here gets a connection to the database, executes a query and formats the results.
'''

import json

from context import logbook_db

from dal.sql_queries import QUERY_SELECT_EXPERIMENTS_FOR_INSTRUMENT, QUERY_SELECT_ELOG_ENTRIES_FOR_EXPERIMENT

__author__ = 'mshankar@slac.stanford.edu'


def get_experiments_for_instrument(instrument_name):
    """
    Return the experiments for a given instrument
    :param instrument_name: The instrument for the experiments, for example, XPP
    :return: List of experiments for this instrument.
    """
    with logbook_db.connect() as cursor:
        cursor.execute(QUERY_SELECT_EXPERIMENTS_FOR_INSTRUMENT, {"instrument_name": instrument_name})
        return cursor.fetchall()


def get_elog_for_experiment(experiment_name):
    """
    Get the elog entries for an experiment. 
    :param experiment_name - for example - diadaq13
    :return: List of elog entries + run start/stop entries for the experiment sorted by descending time.
    """
    with logbook_db.connect() as cursor:
        cursor.execute(QUERY_SELECT_ELOG_ENTRIES_FOR_EXPERIMENT, {"experiment_name": experiment_name})
        return cursor.fetchall()
    