__author__ = 'mshankar@slac.stanford.edu'

# Add all your SQL queries (if any) in this file.
QUERY_SELECT_EXPERIMENTS_FOR_INSTRUMENT = """
SELECT
    experiment.id as experiment_id,
    experiment.name as experiment_name
FROM
    regdb.experiment experiment
JOIN 
    regdb.instrument instrument 
ON  experiment.instr_id = instrument.id
    AND instrument.name = %(instrument_name)s
ORDER BY
    experiment_name
;
"""
