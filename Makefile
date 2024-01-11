all: recipes2rdf units foodweights2rdf format populate update-server-data

recipes2rdf:
	@./tools/csv2rdf \
		--mode annotated \
		--user-metadata metadata/recipes.json \
		--output-file output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/recipes.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/recipes3.rq -i output/recipes.ttl -o output/recipes.ttl

units:
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/ounce.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/cup.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/pounds.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/quarts.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/slices.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/package.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/teaspoons.rq -i output/recipes.ttl -o output/recipes.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/mesurementsQueries/tablespoons.rq -i output/recipes.ttl -o output/recipes.ttl

foodweights2rdf:
	@./tools/csv2rdf \
		--mode annotated \
		--user-metadata ./metadata/food_weights.json \
		--output-file output/food_weights.ttl
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/food_weights.rq -i output/food_weights.ttl -o output/food_weights.ttl

populate:
	@cd data_finder && poetry run python3 data_finder

format:
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q metadata/format.rq -i output/recipes.ttl -o output/recipes.ttl

update-server-data:
	@cp ./vocab/*.ttl ./kitchen_chef_server/data

# TEST (not in pipeline)
conversionentailment:
	@java -jar ./tools/corese-command-4.5.0.jar sparql -q ./metadata/conversionEntailement.rq -i ./vocab/measurements.ttl -o ./vocab/measurements.ttl

server:
	 @cd ./kitchen_chef_server/ && poetry run uvicorn kitchen_chef_server.__main__:app --reload
