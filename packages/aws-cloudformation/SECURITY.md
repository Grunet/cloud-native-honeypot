# AWS Cloudformation - Security

## Warnings

### Take Caution Around the Managed Policies for Creating/Deleting the Honeypot Stack

If compromised, the CreatePolicy could be abused to create a role with an AdministratorAccess policy that's then passed to an EC2 instance, Fargate task, Lambda execution environment, etc...

It's best to only create the CreatePolicy and DeletePolicies ad hoc/as-needed (i.e. counterintuively not as part of a long-lived stack role), and then delete them afterwards.

That way there's no way to compromise them (since they won't exist).

## Tools in Place

### Security Static Analysis

`cfn-guard` with all of the rules from `aws-guard-rules-registry` is the only thing in use at the moment.