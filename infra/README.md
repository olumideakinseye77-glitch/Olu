# Project 2: Automated Azure Deployment with Terraform

This project extends [Project 1](../README.md). Terraform reads the existing resource group, Azure Container Registry and Container Apps environment, then defines a **separate staging quiz** with a user-assigned identity and `AcrPull` access. The live quiz remains outside this Terraform configuration.

## What this demonstrates

- Existing Azure resources are read through Terraform data sources, so the production quiz stays untouched.
- A dedicated user-assigned identity receives the `AcrPull` role scoped to the existing registry.
- A staging Container App runs the same image with 0–1 replicas, public HTTPS ingress and port 8000.
- Terraform state is stored in a private Azure Storage blob container and accessed using Azure CLI Microsoft Entra authentication. State is never committed to GitHub.

## Deployed result

On 25 September 2026, the reviewed plan showed **3 to add, 0 to change, 0 to destroy**. `terraform apply` completed with exactly those three resources: the identity, role assignment, and staging Container App. The staging quiz was played successfully in a browser. A follow-up `terraform plan -no-color` reported **No changes. Your infrastructure matches the configuration.** The Container App pins `workload_profile_name = "Consumption"` to match Azure's reported profile:

**[Open the staging quiz](https://west-africa-quiz-staging.orangetree-477f51ac.uksouth.azurecontainerapps.io)**

The existing production app, Container Apps environment, and registry were read as data sources, with no planned changes.

## State and access

The backend is declared in [backend.tf](backend.tf): storage account `oluwestafricatfstate77`, private container `tfstate`, blob `project2-staging.tfstate`. The storage account is in `rg-west-africa-quiz` in UK South and uses Standard LRS. The Azure account running Terraform needs **Storage Blob Data Contributor** on that storage account, plus rights to manage the staging resources and assign `AcrPull`.

Azure Cloud Shell is ephemeral. A new session must clone this branch, run `terraform init`, and set `TF_VAR_subscription_id` again. The backend persists the state between sessions. State can contain sensitive values; do not add it to GitHub. The account and the staging app may incur Azure charges.

The existing registry uses **LegacyRegistryPermissions**, so `AcrPull` is the relevant role. If that mode changes, revisit the assignment. The `v1` image must remain in the registry.

## Reproduce and check

In Azure Cloud Shell:

```bash
git clone --branch project-2-terraform-staging --single-branch https://github.com/olumideakinseye77-glitch/Olu.git Olu-project2
cd Olu-project2/infra
export TF_VAR_subscription_id="$(az account show --query id -o tsv)"
terraform init
terraform fmt -check
terraform validate
terraform plan -no-color
terraform output staging_url
```

A normal follow-up plan should report **No changes**. Test the URL and `/health` after deployment. If you deliberately change the image tag or another setting, review the new plan before applying it.

## Notes from deployment

- Cloud Shell's first storage data request timed out obtaining a token. Signing in to the subscription's tenant for the storage scope resolved that issue.
- Initial backend access returned `403 AuthorizationPermissionMismatch`. Assigning **Storage Blob Data Contributor** to the signed-in user at the storage-account scope fixed it.
- The first `terraform init` with the backend succeeded; the final plan and apply each showed exactly three creations.
- A follow-up plan initially proposed `workload_profile_name = "Consumption" -> null`. Pinning the observed `Consumption` profile in the configuration removed that drift without changing the running app.

## Next project

Project 3 adds automated tests and a GitHub Actions workflow to build, tag and deploy an image after code changes.
