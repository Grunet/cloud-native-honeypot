# AWS Cloudformation - Readme

## Requirements

### Needs a Route to the Public Internet

The subnet you're deploying `honeypot.yaml` to needs a route to the public internet (e.g. via a NAT Gateway).

This is because the Fargate task is pulling the honeypot container image from ghcr.io (Github Container Registry).

## Guidelines

### Don't Update the Stack, Just Delete it and Create a New One

The `honeypot.yaml` stack is only intended to be created and deleted, not updated.

If you need to deploy a new version of the stack, delete the current one and create the new one.

(Everything in the stack is stateless so this should not be problematic)