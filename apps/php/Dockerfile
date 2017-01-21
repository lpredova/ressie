FROM eboraas/apache
MAINTAINER Ed Boraas <ed@boraas.ca>

RUN apt-get update && apt-get -y install apt-transport-https curl php5 php5-mysql && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN /usr/sbin/a2dismod 'mpm_*' && /usr/sbin/a2enmod mpm_prefork

RUN a2enmod rewrite

RUN mkdir -p /var/www/html
WORKDIR /var/www/html
VOLUME /var/www/html/

# Elastic Beats
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-5.1.2-amd64.deb && dpkg -i filebeat-5.1.2-amd64.deb
ADD ./filebeat.yml /etc/filebeat/filebeat.yml
#RUN /usr/bin/filebeat.sh

EXPOSE 80
EXPOSE 443

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

#RUN /etc/init.d/logstash start

# https://hub.docker.com/r/eboraas/apache-php/~/dockerfile/