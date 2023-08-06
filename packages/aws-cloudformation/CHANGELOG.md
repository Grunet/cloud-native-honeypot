# Changelog

## What constitutes a breaking change?

What is in scope for breaking changes includes (but isn't necessarily limited to)

- Inputs of templates
- Outputs of templates
- Breaking changes in new container image versions (according to their logic for breaking changes)

## Changes

### v0.2.1

- Update honeypot container image from v0.4.4 to v0.4.5

### v0.2.0

- Restrict values for LogRetentionPolicy in the honeypot stack to the values log groups allow so there's feedback before stack creation
- Allow for injecting a KMS key into the honeypot stack to use for the new log group
- Switch to using managed policies instead of inline policies for the task and task execution roles

- (Dev only change) Always use the latest Amazon Linux 2023 image for the basion host
- (Dev only change) Start using cfn-guard for security static analysis

### v0.1.1

- Fix bug that wouldn't let the delete policy work without also having the create policy

### v0.1.0

- Created a Cloudformation template to deploy the honeypot as a single task running in an ECS service
- Created a Cloudformation template declaring IAM policies that can be used to create or delete the template from the previous list item
