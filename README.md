# Ressie SIEM Elastic plugin

<img src="./ressie.png" alt="Ressie" width="170px"> + <img src="http://www.emerce.nl/content/uploads/2016/10/elastic_stack.png" alt="Ressie" width="280px">



Ressie is open source SIEM component for ELK stack, it provides real time monitoring, alerting and threat analysis.

#### Note
**This work is just SIEM proof of concept. Use at your own risk!**

#### Contains
* MySql 5.7 - https://hub.docker.com/_/mysql/
* Ubuntu + Php 5.6 + Apache 2 + (filebeat & networkbeat)
* ElasticSearch 5 
* Logstash 5 
* Kibana 5
* MySql 5.7 - ressie operational db

#### Features
* Custom alerting (email, slack..)
* Indexed Fuzz DB for full text search attack database
* Custom configuration of service 
* Pattern matching
* IP validation against TOR and VirusTotal

**TODO**:

* concurrent process (threading, workers)
* UI
* machine learning implementation
* suspicious usage monitor
* TBD...

## Installation

Navigate to project root

```
$ cd ./ressie
```

### Requirements & Configuration

* Docker
* Docker-compose
* MySQL database server (locally for ressie data)

Create and configure variables.env file based on variables.env.example

```
PostgreSQL settings

POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
PGDATA=/var/lib/postgresql/data/pgdata

MySQL settings
MYSQL_ROOT_PASSWORD=secret
MYSQL_DATABASE=databaseName
MYSQL_USER=databaseUser
MYSQL_PASSWORD=databaseSecret
```


## Usage

####Run architecture

Navigate to **project** root

```
$ cd ./ressie
```

```
$ docker-composer up
```

To put logs directly to Elasticsearch use:

```
$ nc localhost 5000 < /path/to/logfile.log
```

#### Run App

Setup services from config:

```
$ cd ./ressie/ressie/configurations/
```

* Name file config.prod 

* Use example from [HERE](https://github.com/lpredova/ressie/blob/master/ressie/ressie/configurations/config.example) to write new config file based on your credentials and preferences
* Save  :tada:



Navigate to **app** root

```
$ cd ./ressie
```

Then run:

```python
$ python -m help

```


### References

Big  :clap:  to:


* [Adam Muntner - Fuzz DB project](https://github.com/fuzzdb-project/fuzzdb/) - used for patterns recognition
* [Anthony Lapenna - Docker ELK stack](https://devhub.io/repos/deviantony-docker-elk) - used for base of test architecture

---
**Lovro Predovan**
2017
