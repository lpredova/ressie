#!/bin/bash

service filebeat start
service packetbeat start
/usr/sbin/apache2ctl start

tail -f /var/log/dmesg