#!/bin/bash
java \
  -Dfile.encoding="UTF-8"\
  -jar corese-server.jar \
  -p 8080 \
  -lp \
  -pp /usr/local/corese/config/corese-profile.ttl \
  -init /usr/local/corese/config/corese-properties.properties
