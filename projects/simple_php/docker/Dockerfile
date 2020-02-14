# Dockerfile: Simple PHP

# Pull base image
FROM ubuntu:latest

# Non-interactive
ENV DEBIAN_FRONTEND noninteractive

# COPY run_server.sh
COPY run_server.sh /bin
RUN chmod +x /bin/run_server.sh

# apt-get update
RUN apt-get update

# install apache, php, mysql
RUN apt-get install -y php php-mysqli libapache2-mod-php mysql-server

# enable mysql service
COPY mysql.sql /etc/mysql.sql
RUN service mysql start && mysql < /etc/mysql.sql