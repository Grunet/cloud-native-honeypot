
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
