all: recipes2rdf foodweights2rdf units
recipes2rdf:
	@./tools/csv2rdf \
		--mode annotated \
		--user-metadata metadata/recipes.json \
		--output-file output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/recipes.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/recipes3.rq -i output/recipes.ttl -o output/recipes.ttl

units:
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/recipes2.rq -i output/recipes.ttl -o output/recipes.ttl

foodweights2rdf:
	@./tools/csv2rdf \
		--mode annotated \
		--user-metadata ./metadata/food_weights.json \
		--output-file output/food_weights.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/food_weights.rq -i output/food_weights.ttl -o output/food_weights.ttl

populate:
	cd data_finder && poetry run python3 data_finder

format:
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/format.rq -i vocab/recipes.ttl -o vocab/recipes.ttl
