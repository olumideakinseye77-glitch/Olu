terraform {
  backend "azurerm" {
    storage_account_name = "oluwestafricatfstate77"
    container_name       = "tfstate"
    key                  = "project2-staging.tfstate"
    use_azuread_auth     = true
    use_cli              = true
  }
}
