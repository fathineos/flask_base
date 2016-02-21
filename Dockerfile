FROM fathineos/debian_base:latest

# Sets the python virtualenv location
ENV ENV /opt/venv
VOLUME ["/srv/www/base/current"]

# Temporary app location, necessary to install dependencies
ADD ./ /srv/www/base/frozen
WORKDIR /srv/www/base/frozen

RUN apt-get update -qq &&\
    make -f docker/Makefile all &&\
    apt-get clean &&\
    rm -rf /srv/www/base/frozen

# The location where the application data volume will be mounted
WORKDIR /srv/www/base/current
EXPOSE 6000

ADD docker/init.sh /init.sh
RUN chmod 755 /init.sh

# ENTRYPOINT ["entrypoint.sh"]

CMD ["/init.sh"]
