output "staging_url" {
  description = "URL to test the Terraform-managed staging deployment."
  value       = "https://${azurerm_container_app.staging.ingress[0].fqdn}"
}

output "staging_identity_id" {
  description = "User-assigned managed identity used for image pulls."
  value       = azurerm_user_assigned_identity.staging.id
}
