# cloud-native-honeypot

Honeypots made for a cloud native world.

## Quickstart

### Deploying the Honeypot

1. Pick an AWS VPC you want to deploy the honeypot to
2. Pick a subnet from that VPC to deploy the honeypot to
3. Get the `honeypot.yaml` Cloudformation stack template from the latest of the [aws-cloudformation Github Releases](https://github.com/Grunet/cloud-native-honeypot/releases?q=aws-cloudformation&expanded=true)
4. Deploy the stack template, inputting the VPC id and subnet id as stack parameters

You should get 1 Fargate task running on ECS for the honeypot itself and an associated Eventbridge event bus.

### Reacting to Events Published by the Honeypot

When hit with GET requests, the task will publish events to the event bus. 

You can add an Evenbridge rule to the event bus to react to the events.

For example, you could add a rule targeting events with source `cloud-native-honeypot` that invokes an SNS topic, which then notifies humans of the events.


