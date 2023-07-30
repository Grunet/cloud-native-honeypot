# AWS Cloudformation

## Test AWS Account

The account for testing was setup as a single account with

- A root user with MFA enabled
- An IAM user with AdministratorAccess and MFA enabled
- A [billing alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html)

Per region maunal setup was as follows

- SSM was enabled for instances by default by turning on [Default Host Management Configuration](https://docs.aws.amazon.com/systems-manager/latest/userguide/managed-instances-default-host-management.html) in Fleet Manager (there appears to be no Cloudformation support for this based off of https://github.com/aws-samples/aws-systems-manager-default-host-management-configuration/blob/main/enableDefaultHostManagement.yml falling back to calling AWS APIs directly).
    - A new instance management IAM role (the default proposed by the UI) was created in the process