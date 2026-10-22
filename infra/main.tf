# Read Project 1 resources. Terraform will not try to replace them.
data "azurerm_resource_group" "existing" {
  name = var.resource_group_name
}

data "azurerm_container_app_environment" "existing" {
  name                = var.environment_name
  resource_group_name = data.azurerm_resource_group.existing.name
}

data "azurerm_container_registry" "existing" {
  name                = var.registry_name
  resource_group_name = data.azurerm_resource_group.existing.name
}

# Give only the staging app a managed identity that can pull its image.
resource "azurerm_user_assigned_identity" "staging" {
  name                = "id-west-africa-quiz-staging"
  location            = data.azurerm_resource_group.existing.location
  resource_group_name = data.azurerm_resource_group.existing.name
}

resource "azurerm_role_assignment" "staging_acr_pull" {
  scope                = data.azurerm_container_registry.existing.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.staging.principal_id
  principal_type       = "ServicePrincipal"
}

# Deploy the same Docker image as a separate staging app.
resource "azurerm_container_app" "staging" {
  name                         = var.staging_app_name
  container_app_environment_id = data.azurerm_container_app_environment.existing.id
  resource_group_name          = data.azurerm_resource_group.existing.name
  revision_mode                = "Single"
  workload_profile_name       = "Consumption"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.staging.id]
  }

  registry {
    server   = data.azurerm_container_registry.existing.login_server
    identity = azurerm_user_assigned_identity.staging.id
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "quiz"
      image  = "${data.azurerm_container_registry.existing.login_server}/west-africa-quiz:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    external_enabled           = true
    target_port                = 8000
    transport                  = "auto"
    allow_insecure_connections = false

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  depends_on = [azurerm_role_assignment.staging_acr_pull]
}
