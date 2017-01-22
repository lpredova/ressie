#!/bin/bash

service filebeat start
/usr/sbin/apache2ctl start

tail -f /var/log/dmesg