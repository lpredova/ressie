#!/usr/bin/env bash

set -e
service mysql start
mysql < /mysql/ressie.sql
service mysql stop