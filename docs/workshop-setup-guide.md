# Workshop Setup Guide — Foundry Agents Essentials (Legal)

This guide is for **IT administrators and workshop organizers** who need to prepare the Azure environment before participants arrive. It covers what to provision, what permissions to grant, and what the workshop deployment (`azd up`) handles automatically.

---

## Overview

Each participant will:

1. Clone the repository
2. Run `azd up` to deploy infrastructure and application code
3. Work through 8 units in the Microsoft Foundry portal (no code required)

The deployment creates Azure resources and assigns data-plane roles automatically. Your job is to ensure participants have the right subscription-level access **before** they begin.

---

## Step 1: Azure Subscription & Resource Group Setup

### Option A — Shared Subscription, Individual Resource Groups (Recommended)

Create one resource group per participant. This provides isolation and easy cleanup.

```
rg-workshop-participant01
rg-workshop-participant02
...
```

### Option B — Individual Subscriptions

Each participant uses their own Azure subscription. They must have **Owner** (or **Contributor** + **User Access Administrator**) on the subscription.

---

## Step 2: Grant Permissions (Before the Workshop)

Each participant needs the following roles on their resource group **before** running `azd up`:

| Role | Why | Grants |
|------|-----|--------|
| **Owner** (or **Contributor** + **User Access Administrator**) | Creates resources + assigns RBAC roles during deployment | Full management-plane access + `Microsoft.Authorization/roleAssignments/write` |

> **Why Owner?** The `azd up` deployment creates role assignments via Bicep (assigning `Cognitive Services User`, `Azure AI User`, and `Azure AI Account Owner` to both the App Service managed identity and the participant). The **Contributor** role cannot create role assignments — only **Owner** (or Contributor + User Access Administrator) can.

**If Owner is not possible**, assign both of these:

| Role | Why |
|------|-----|
| **Contributor** | Create and manage all Azure resources |
| **User Access Administrator** | Create the role assignments in the Bicep templates |

### How to Assign

**Azure Portal:**
1. Navigate to the resource group → **Access control (IAM)** → **Add role assignment**
2. Select **Owner** (or both **Contributor** and **User Access Administrator**) → **Members** → search for the participant's Entra ID account → **Assign**

**Azure CLI (bulk assignment):**
```bash
az role assignment create \
  --assignee <participant-email-or-object-id> \
  --role "Owner" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

# Or, if using Contributor + User Access Administrator:
az role assignment create \
  --assignee <participant-email-or-object-id> \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

az role assignment create \
  --assignee <participant-email-or-object-id> \
  --role "User Access Administrator" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>
```

---

## Step 3: Verify Tooling Prerequisites

Ensure participants have the following installed on their machines **before** the workshop:

| Tool | Version | Installation |
|------|---------|-------------|
| [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) | Latest | `winget install microsoft.azd` |
| [Python](https://www.python.org/downloads/) | 3.11+ | Required for backend deployment |
| [Node.js](https://nodejs.org/) | 18+ | Required for frontend build during deployment |
| [Git](https://git-scm.com/) | Latest | Clone the repository |
| Modern browser | Edge or Chrome | Access Foundry portal and tracker dashboard |

> **💡 Tip:** If participants use company-managed machines with restricted installs, consider providing pre-configured VMs or Dev Boxes with all tools pre-installed.

---

## What `azd up` Creates (Automatically)

When a participant runs `azd up`, the following resources are provisioned:

| Resource | Type | Purpose |
|----------|------|---------|
| **App Service Plan** | PremiumV3 (P0v3), Linux | Hosts the web app |
| **Web App** | Python 3.11, system-assigned managed identity | Onboarding tracker (FastAPI backend + React frontend + MCP server) |
| **AI Services Account** | S0, kind: AIServices | Foundry account for agents, models, and evaluation |
| **Foundry Project** | `onboarding-lab` | Workspace for agents and workflows |
| **Bing Grounding Resource** | G1, global | Grounding with Bing for web search |
| **Bing Connection** | Shared to all project users | Connects the Bing resource to the Foundry account |

### Role Assignments Created by `azd up`

These are assigned automatically during deployment — no manual action needed:

| Principal | Role | Scope | Purpose |
|-----------|------|-------|---------|
| **App Service managed identity** | Cognitive Services User | Foundry account | Backend can call AI Services endpoints |
| **App Service managed identity** | Azure AI User | Foundry account | Backend can interact with Foundry APIs |
| **App Service managed identity** | Azure AI Account Owner | Foundry account | Consistent role set across all principals |
| **Participant (deployer)** | Cognitive Services User | Foundry account | Use model deployments in the portal |
| **Participant (deployer)** | Azure AI User | Foundry account | Create agents, deploy models, create workflows, use playground |
| **Participant (deployer)** | Azure AI Account Owner | Foundry account | Create and configure guardrails (Unit 7) |

### What's NOT Assigned by `azd up`

All roles required for the workshop are now assigned automatically by `azd up`. No manual role assignments are needed.

---

## Quick Reference: Complete Permission Matrix

| Phase | Role | Scope | Who Assigns |
|-------|------|-------|-------------|
| **Pre-workshop** | Owner (or Contributor + User Access Administrator) | Resource group | IT admin / organizer |
| **During `azd up`** | Cognitive Services User | Foundry account | Bicep (automatic) |
| **During `azd up`** | Azure AI User | Foundry account | Bicep (automatic) |
| **During `azd up`** | Azure AI Account Owner | Foundry account | Bicep (automatic) |

---

## Estimated Azure Costs

| Resource | Estimated Cost | Notes |
|----------|---------------|-------|
| App Service (P0v3) | ~$75/month | Can scale down to B1 for cost savings |
| AI Services (S0) | Pay-per-use | Model usage billed per token |
| Bing Grounding (G1) | ~$3/1000 transactions | Minimal usage during workshop |
| **Total per participant** | **~$5–10 for a single-day workshop** | Assuming moderate playground usage |

> **💡 Tip:** Delete the resource groups immediately after the workshop to stop all charges. Run `azd down` from each participant's machine, or bulk-delete the resource groups from the Azure Portal.

> **💰 Note:** The AI Services account (Foundry) is purely pay-per-use — there is no standing charge while idle. If you want participants to continue exploring Foundry after the workshop, you can safely leave the AI Services resource running and only delete the App Service Plan to eliminate the primary fixed cost.

---

## Post-Workshop Cleanup

```bash
# Each participant can clean up their own resources:
azd down --purge --force

# Or the admin can bulk-delete resource groups:
az group delete --name rg-workshop-participant01 --yes --no-wait
az group delete --name rg-workshop-participant02 --yes --no-wait
```

> **⚠️ Important:** The `--purge` flag permanently deletes soft-deleted AI Services resources. Without it, the resource names may be reserved for up to 48 hours, blocking reuse.
