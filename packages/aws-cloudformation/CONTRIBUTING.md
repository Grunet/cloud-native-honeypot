# AWS Cloudformation - Contributing

## Notes on Testing

The templates are currently organized as follows

1. `bootstrap.yaml` - Sets up a VPC and subnets and 1 EC2 instance to SSM into
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