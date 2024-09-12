#!/bin/sh

IP_ADDRESS=$(hostname -I | awk '{print $1}')

export DYNAMIC_IP=$IP_ADDRESS

exec uvicorn app.main:app --host 0.0.0.0 --port 8123