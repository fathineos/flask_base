FROM fathineos/debian_base:latest

# Sets the python virtualenv location
ENV ENV /opt/venv
VOLUME ["/srv/www/base/current"]

# Temporary app location, necessary to install dependencies
ADD ./ /srv/www/base/frozen
WORKDIR /srv/www/base/frozen

RUN apt-get update -qq &&\
    make _install_system_dependencies &&\
    make _create_virtualenvironment &&\
    make _install_application_dependencies &&\
    make _install_development_application_dependencies &&\
    mkdir /srv/www/base/configs/ &&\
    make _generate_docker_production_configuration_files &&\
    make _generate_docker_development_configuration_files &&\
    apt-get clean &&\
    rm -rf /srv/www/base/frozen

# The location where the application data volume will be mounted
WORKDIR /srv/www/base/current
EXPOSE 6000

ADD docker/init.sh /init.sh
RUN chmod 755 /init.sh

# ENTRYPOINT ["entrypoint.sh"]

CMD ["/init.sh"]
