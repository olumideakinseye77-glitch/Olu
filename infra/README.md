# Project 2: Automated Azure Deployment with Terraform

This project extends [Project 1](../README.md). Terraform reads the existing resource group, Azure Container Registry and Container Apps environment, then defines a **separate staging quiz** with a user-assigned identity and `AcrPull` access. The live quiz remains outside this Terraform configuration.

## Why staging?

Project 1's live app works and uses the environment's managed identity. The AzureRM Container App resource documents a user-assigned identity for its registry configuration. A new staging app lets you learn Terraform with an explicit identity and an isolated deployment. It also avoids another container registry and another environment. The staging app and identity can still incur charges; review `terraform plan` and Azure pricing before applying.

## What you will learn

1. Read existing Azure resources with Terraform data sources.
2. Declare an identity and narrowly scoped registry pull role.
3. Declare a Container App with one image, 0–1 replicas, and public ingress to port 8000.
4. Use `terraform init`, `fmt`, `validate`, `plan`, and `apply` with a durable state backend.
5. Change the image tag as a controlled deployment, verify `/health`, and document the plan and live staging URL.

## Before applying

**Terraform state must be durable.** Your Azure Cloud Shell session is ephemeral, so do not run `terraform apply` there with local state. State can contain sensitive data and must never be committed to GitHub.

Create an Azure Storage account with a private blob container for Terraform state, or use another durable Terraform backend. For Azure Storage, add `backend "azurerm" {}` inside the `terraform` block in `versions.tf`, then supply the backend's resource group, storage account, container, key and Azure AD authentication through a local `backend.hcl` file (which is ignored by Git). Consult the [Azure state backend guide](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/store-state-in-azure-storage) for the exact setup and permissions. Storage may incur charges.

The existing registry uses **LegacyRegistryPermissions**, so `AcrPull` is the relevant role. If that mode is changed, revisit the role assignment. You need Azure rights to create a managed identity, assign `AcrPull`, and deploy a Container App. The `v1` image must still exist in the existing registry.

## Safe preparation commands

Install Terraform and sign in to the Azure CLI on your computer, or use Azure Cloud Shell for validation only. From `infra/`:

```bash
terraform fmt -check
terraform init -backend=false
terraform validate
```

These commands should not create Azure resources. Once durable state is configured and the correct subscription is selected:

```bash
export TF_VAR_subscription_id="$(az account show --query id -o tsv)"
terraform init -backend-config=backend.hcl
terraform plan -out=staging.tfplan
```

Review the plan: it should create **only** one user-assigned identity, one `AcrPull` role assignment, and one **staging** Container App. It should not modify the live app, existing environment, or existing registry. Apply only after reviewing the plan and costs:

```bash
terraform apply staging.tfplan
terraform output staging_url
```

Test the staging URL and `/health`. Keep the state backend and its access safe so future plans know what Terraform created.

## Definition of done

- `terraform validate` passes.
- A reviewed plan shows the three intended staging resources only.
- The staging quiz and `/health` work through the public URL.
- A second `terraform plan` shows no changes.
- This README records the plan, output URL, and any deployment fixes.

## Next project

Project 3 adds automated tests and a GitHub Actions workflow to build, tag and deploy an image after code changes. Project 2 deliberately focuses on repeatable infrastructure and state.
