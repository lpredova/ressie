FROM mysql:5.7

RUN apt-get update && apt-get -y install apt-transport-https curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Elastic Beats
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-5.1.2-amd64.deb && dpkg -i filebeat-5.1.2-amd64.deb
ADD ./filebeat.yml /etc/filebeat/filebeat.yml

ADD start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]