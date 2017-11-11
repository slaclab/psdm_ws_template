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

QUERY_SELECT_ELOG_ENTRIES_FOR_EXPERIMENT = """
SELECT 
 e.insert_time DIV 1000000000 AS insert_time, e.author AS author, e.content AS text, e.content_type AS content_type, run.num AS run_num
FROM       entry e 
INNER JOIN header h ON e.hdr_id = h.id
INNER JOIN regdb.experiment exp ON h.exper_id = exp.id AND exp.name = %(experiment_name)s
LEFT JOIN  run run ON h.run_id = run.id
WHERE exp.name = 'diadaq13'
ORDER BY insert_time DESC;
"""
