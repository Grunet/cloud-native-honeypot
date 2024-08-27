variable "vpc_id" {
  type        = string
  description = "The VPC to place the honeypot service in"
}

variable "subnet_id" {
  type        = string
  description = "The subnet to place the honeypot service in"
}

variable "cluster_name_or_arn" {
  type        = string
  default     = ""
  description = "The name or ARN of an existing ECS cluster the honeypot service should be added to (instead of creating a new cluster)"
}

# Used to make names of resources unique, allowing for this module to be re-used multiple times in the same region
resource "random_uuid" "unique_suffix" {
}

resource "aws_ecs_cluster" "cluster" {
  count = var.cluster_name_or_arn != "" ? 0 : 1

  name = "cluster-${random_uuid.unique_suffix.result}"

  tags = {
    cloud-native-honeypot = true
  }
}

resource "aws_ecs_service" "service" {
  name = "service-${random_uuid.unique_suffix.result}"

  cluster                 = var.cluster_name_or_arn != "" ? var.cluster_name_or_arn : aws_ecs_cluster.cluster.name
  desired_count           = 1
  enable_ecs_managed_tags = true
  launch_type             = "FARGATE"
  network_configuration {
    assign_public_ip = false
    subnets          = [var.subnet_id]
    security_groups  = [aws_security_group.sg_ingress_full_access]
  }
  platform_version = "1.4.0"
  propagate_tags   = "SERVICE"
  tags = {
    cloud-native-honeypot = true
  }
  # TODO - need to fill this reference out
  # task_definition = ""
}

resource "aws_security_group" "sg_ingress_full_access" {
  description = "Allows all ingress traffic from within the VPC"
  ingress = [
    {
      cidr_blocks = ["0.0.0.0/0"]
      protocol    = -1
      from_port   = 0
      to_port     = 0
    }
  ]
  tags = {
    cloud-native-honeypot = true
  }
  vpc_id = var.vpc_id
}
