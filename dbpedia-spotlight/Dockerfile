FROM ubuntu:22.04
MAINTAINER  DBpedia Spotlight Team <dbp-spotlight-developers@lists.sourceforge.net>

ENV SPOTLIGHT  https://sourceforge.net/projects/spotlight-multilingual-docker/files/dbpedia-spotlight-1.1.jar

# adding required packages
RUN apt update && apt upgrade -y && \
    apt install -y bash && apt install -y openjdk-8-jre && \
    apt install -y tshark && apt install -y wget && \
    apt install -y curl && apt clean

# downloading spolight model and dbpedia spotlight
RUN mkdir -p /opt/spotlight/models && \
   cd /opt/spotlight && \
   wget -O dbpedia-spotlight.jar $SPOTLIGHT && \
   mkdir -p src/main/resources/templates/

# adding the script to the container
ADD spotlight.sh /bin/spotlight.sh
COPY nif-21.vm /opt/spotlight/src/main/resources/templates/nif-21.vm
RUN chmod +x /bin/spotlight.sh

EXPOSE 80
