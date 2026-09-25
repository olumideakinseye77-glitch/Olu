variable "subscription_id" {
  description = "Azure subscription ID. Supply through TF_VAR_subscription_id."
  type        = string
}

variable "resource_group_name" {
  description = "Existing resource group from Project 1."
  type        = string
  default     = "rg-west-africa-quiz"
}

variable "environment_name" {
  description = "Existing Container Apps environment from Project 1."
  type        = string
  default     = "managedEnvironment-rgwestafricaqui-a029"
}

variable "registry_name" {
  description = "Existing Azure Container Registry from Project 1."
  type        = string
  default     = "oluwestafricaquiz"
}

variable "image_tag" {
  description = "An image tag already pushed to the existing registry."
  type        = string
  default     = "v1"
}

variable "staging_app_name" {
  description = "Name for the additional staging Container App."
  type        = string
  default     = "west-africa-quiz-staging"
}
