# AWS Cloudformation - Readme

## Guidelines

### Don't Update the Stack, Just Delete it and Create a New One

The `honeypot.yaml` stack is only intended to be created and deleted, not updated.

If you need to deploy a new version of the stack, delete the current one and create the new one.

(Everything in the stack is stateless so this should not be problematic)