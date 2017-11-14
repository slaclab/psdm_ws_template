# psdm-ws-template
Template for psdm services

* Uses Python 3.




http://localhost:5000//ws/business/XPP/experiments


http://localhost:17669/psdm/experiments/XPP

http://localhost:17669/psdm/diadaq13/elog

curl -XPOST "http://localhost:17669/psdm/ws/business/diadaq13/elog" -H 'Content-Type: application/json' -d'{ "content" : "Test from the command line 6", "content_type": "TEXT", "run_num": 8 }'