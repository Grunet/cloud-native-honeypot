# AWS Cloudformation

## Contributing

### Notes on Testing

The templates are currently organized as follows

1. `bootstrap.yaml` - Sets up a VPC and subnets and 1 ECS instance to SSM into
2. `honeypot.yaml` - Deploys an ECS service with the honeypot and an EventBridge event bus
3. `events_to_logs.yaml` - Deploys a rule to convert events published to the event bus to logs

These 3 can be created in this order for testing purposes.

To test the stack policies, a stack role can be created from these templates

1. `honeypot-stack-policies.yaml` - Creates 2 policies for creating and deleting the `honeypot.yaml` template
2. `stack-role.yaml` - Creates a Cloudformation stack role from the 2 policies

Adding this role as a stack role when deploying the `honeypot.yaml` template can be done for testing purposes.

## Test AWS Account

The account for testing was setup as a single account with

- A root user with MFA enabled
- An IAM user with AdministratorAccess and MFA enabled
- A [billing alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html)

## Dependency Maintenance

This goes over the maintenance needs and strategies for this subproject.

### Maintenance Needs

The following is an overview of all the areas that may need patches and updates:

- Devcontainer
    - (Ubuntu base image is covered by the honeypot subproject)
    - cfn-lint version
    - cfn-guard version
- Github Workflows
    - (Ubuntu runner versions is covered by the honeypot subproject)
    - 3rd party action versions
    - cfn-lint version
    - cfn-guard version
    - Version of binaries (e.g. cosign, curl, jq)
- Testing Tools
    - Bastion EC2 AMI
    - Vendored guard-rules-registry-all-rules.guard file
- This Package's Contents
    - PlatformVersion in the ECS Service
    - Honeypot container image version (from the other subproject)

### Maintenance Targets

By default, the target for each area is

- Be on the latest major version that has been out for a while

with the exceptions being

- cfn-lint (this is continuously updated based on changes to the AWS API, so needs to be at or near the latest version always to be most useful)
- Vendored guard-rules-registry-all-rules.guard file (this receives new security rules with minor releases that are helpful to pick up)
- Bastion EC2 AMI (this will always pull in the latest version of the image)
- Honeypot container image (immediately after a new image is published, the Cloudformation template should always be updated to the new version and a new Github release created with it)
- Well-known binaries (e.g. curl, jq, that don't strictly need their versions pinned as much)

The goals here are twofold

- To stay away from end-of-life and lack of security support situations
- To always be able to easily uptake security patches without needing to worry about breaking changes at the same time

### Maintenance Strategy

On a monthly basis, I will check to see if any area is not hitting its target and attempt to rectify that

#### cfn-lint

The first step is to check if there is a new release available. This can be done as follows

1. Navigate to https://github.com/aws-cloudformation/cfn-lint/releases
2. Check for any releases newer than the one used in the repo 
    - If there are none, nothing more needs to be done
    - If there are, continue
3. Take the version of the latest release and update it in
    - .devcontainer/Dockerfile
    - ci.yaml
4. Run `make lint`
5. Work through any breaking changes in functionality

From there, update the changelog, and (potentially) bump the version and run the release workflow to publish the changes.

#### cfn-guard

The first step is to check if there is a new release available. This can be done as follows

1. Navigate to https://github.com/aws-cloudformation/cloudformation-guard/releases
2. Check for any releases newer than the one used in the repo (by a major version or more)
    - If there are none, nothing more needs to be done
    - If there are, continue
3. Take the version of the latest release and update it in
    - .devcontainer/Dockerfile
    - ci.yaml
4. Run `make static-analysis-guard`
5. Work through any breaking changes in functionality

From there, update the changelog, and (potentially) bump the version and run the release workflow to publish the changes.

#### Vendored guard-rules-registry-all-rules.guard file

The first step is to check if there is a new file available upstream. This can be done as follows

1. Navigate to https://github.com/aws-cloudformation/aws-guard-rules-registry/releases
2. Check for any new releases since last time
    - If there are none, nothing more needs to be done
    - If there are, continue
3. Download the `ruleset-build` file from the latest release
4. Unzip the zip archive and look for the `guard-rules-registry-all-rules.guard` file
5. Overwrite copy it into the repo
    - If there are no changes, nothing more needs to be done
    - If there are, continue
6. Run `make static-analysis-guard`
7. Resolve any new violations that come up
8. Commit the changes

From there, update the changelog, and (potentially) bump the version and run the release workflow to publish the changes.

#### PlatformVersion in the ECS Service

The first step is to check if there is a new PlatformVersion available. This can be done as follows

1. Navigate to https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform-linux-fargate.html
2. Check the page for any versions newer that the PlatformVersion in `honeypot.yaml`
3. If there is a newer version (not very recently released), update `honeypot.yaml` and smoke test the changes

From there, update the changelog, bump the version, and run the release workflow to publish the changes.

#### 3rd Party Github Actions

Dependabot should be configured to create monthly PRs for any outdated actions, so just need to review and merge those in.

It should be ignoring all (non-security) patch and minor updates, but in case it isn't this should be controllable on each PR that comes in (there should be an option to make it that way for each particular dependency).

### Learning About and Taking Security Patches

Picking up security patches requires first learning about them in the first place. These are the strategies for doing that with the dependencies.

#### cfn-lint

A watch for releases and security alerts was turned on for https://github.com/aws-cloudformation/cfn-lint

#### cfn-guard

A watch for releases and security alerts was turned on for https://github.com/aws-cloudformation/cloudformation-guard

#### Vendored guard-rules-registry-all-rules.guard file

A watch for releases and security alerts was turned on for https://github.com/aws-cloudformation/aws-guard-rules-registry

#### PlatformVersion in the ECS Service

The `check-for-updated-dependencies.yaml` tries to detect any newly released platform versions for Fargate.

#### 3rd Party Github Actions

Dependabot should be creating notices for these.