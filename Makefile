.PHONY: setup_database scrape_data parse_raw_data

#################################################################################
# GLOBALS                                                                       #
#################################################################################

DB_NAME = i_feel


#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Generate all data, setup database, etc
data: setup_database scrape_data parse_raw_data


## Scrape raw data from Reddit and store it in a Postgres db
scrape_data:
	python src/scrape_data.py --start 2010-01-01 --end 2018-01-01

## Parse the scraped data and write it to new table in db
parse_raw_data:
	python src/parse_feelings.py parsed_feelings

## Setup the proper Postgres database table; WILL DELETE DATA!
setup_database:
	DROPDB $(DB_NAME) --if-exists
	CREATEDB $(DB_NAME)
	psql $(DB_NAME) < src/create_table.sql

## Dump database 
dump_database:
	pg_dump $(DB_NAME) -O -F c > data/raw/backup.dump

## Load database dump generated from `dump_database`
load_dump:
	pg_restore -c --if-exists --no-acl --no-owner -d $(DB_NAME) data/raw/backup.dump




#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
#   * save line in hold space
#   * purge line
#   * Loop:
#       * append newline + line to hold space
#       * go to next line
#       * if line starts with doc comment, strip comment character off and loop
#   * remove target prerequisites
#   * append hold space (+ newline) to line
#   * replace newline plus comments by `---`
#   * print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) == Darwin && echo '--no-init --raw-control-chars')
