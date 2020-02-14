#############################
# Dockerfile: Wordpress PHP #
#############################


# Pull base image
FROM simple_php

COPY mysql_wordpress.sql /etc/mysql_wordpress.sql
RUN service mysql start && mysql < /etc/mysql_wordpress.sql