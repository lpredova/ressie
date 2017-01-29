#!/bin/bash

service filebeat start
service mysql start

tail -f /var/log/dmesg