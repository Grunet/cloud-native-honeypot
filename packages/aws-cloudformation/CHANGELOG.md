# Changelog

## What constitutes a breaking change?

What is in scope for breaking changes includes (but isn't necessarily limited to)

- Inputs of templates
- Outputs of templates
- Breaking changes in new container image versions (according to their logic for breaking changes)

## Changes

### v0.1.1

- Fix bug that wouldn't let the delete policy work without also having the create policy

### v0.1.0

- Created a Cloudformation template to deploy the honeypot as a single task running in an ECS service
- Created a Cloudformation template declaring IAM policies that can be used to create or delete the template from the previous list item
