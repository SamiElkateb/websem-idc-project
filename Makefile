csv2rdf:
	@./tools/csv2rdf \
		--mode annotated \
		--user-metadata metadata/transformation.json \
		--output-file output/data.ttl
