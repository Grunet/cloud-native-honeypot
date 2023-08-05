SHELL:=/bin/bash -O globstar # Needed to make sure the glob below finds file at the root of the folder

lint:
	cfn-lint ./templates/**/*.yaml
static-analysis-guard: # Only focusing on the templates that get published to consumers for now
	cfn-guard validate \
		--rules ./guard-rules-registry-all-rules.guard \
		--data ./templates/honeypot.yaml \
		--data ./templates/honeypot-stack-policies.yaml \
		--show-summary all