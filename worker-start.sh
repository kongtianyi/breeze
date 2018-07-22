#!/bin/bash

log_file_name="./worker.log"
pid_file_name="./worker.pid" 
celery -A mysite worker -l info -D -f ${log_file_name} --heartbeat-interval=60 --pidfile=${pid_file_name}