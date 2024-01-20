FROM openjdk:11-jre-slim

WORKDIR /usr/src/app

ADD "https://files.inria.fr/corese/distrib/corese-server-4.5.0.jar" /usr/src/app/corese-server.jar

COPY data/*.ttl /usr/src/app/data/
COPY config /usr/src/app/config
COPY ./entrypoint.sh /entrypoint.sh

# CMD ["java", "-jar", "corese-server.jar", "-l", "data/*.ttl"]

# CMD ["java", "-Dfile.encoding='UTF-8'", "-jar", "corese-server.jar", "-l", "data/categories.ttl", "-l", "data/entailment.ttl", "-l", "data/fix_entaiment.ttl", "-l", "food_thesaurus.ttl", "-l", "measurements.ttl", "-l", "nutrients.ttl", "-l", "recipes.ttl", "-l", "schema.ttl", "-init", "/usr/src/app/config/corese-default-properties.properties"]
ENTRYPOINT ["/entrypoint.sh"]
