csv2rdf:
	@./tools/csv2rdf \
		--mode annotated \
		--user-metadata metadata/recipes.json \
		--output-file output/data.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/recipes.rq -i output/data.ttl -o output/data.ttl
