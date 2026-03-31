# Foundry Agents Essentials

A hands-on workshop for learning AI Agents with Microsoft Foundry. Build an intelligent client onboarding assistant that can search the web, understand documents, and manage real projects — no coding required.

## What You'll Build

A **Client Onboarding Tracker** (Python + React) with an MCP server that a Foundry agent uses to create onboardings, update status, and add notes — demonstrating how AI agents take real actions in business workflows.

**Scenario:** You progressively build one agent — a Client Onboarding Assistant — that helps professional services firms onboard new clients and engagements. Whether you're in legal, construction, or consulting, the onboarding pattern is the same: collect information, check compliance, create the engagement, and track progress.

## Lab Units

| Unit | Topic | Description |
|------|-------|-------------|
| [Unit 1](docs/unit-1-declarative-agent.md) | Declarative Agent | Create your first agent in Microsoft Foundry |
| [Unit 2](docs/unit-2-grounding-with-bing.md) | Grounding with Bing | Add web knowledge so the agent can research clients and regulations |
| [Unit 3](docs/unit-3-knowledge-grounding-files.md) | Knowledge Grounding | Ground your agent with firm policy documents |
| [Unit 4](docs/unit-4-knowledge-bases.md) | Knowledge Bases | Build knowledge bases with multiple sources |
| [Unit 5](docs/unit-5-instructions-and-flow.md) | Instructions & Flow | Craft structured onboarding prompts and conversational design |
| [Unit 6](docs/unit-6-content-understanding.md) | Content Understanding | Extract fields from proposals and classify documents |
| [Unit 7](docs/unit-7-mcp-tools.md) | MCP Tools & Actions | Control the onboarding tracker via agent tool calls |
| [Unit 8](docs/unit-8-workflow-agents.md) | Workflow Agents | Build multi-step onboarding workflows |
| [Unit 9](docs/unit-9-safety-and-governance.md) | Safety & Governance | Apply responsible AI patterns and safety controls |
| [Unit 10](docs/unit-10-evaluation-and-observability.md) | Evaluation & Observability | Trace agent reasoning and evaluate quality |

## Prerequisites

- Azure subscription with **Owner** or **Contributor + User Access Administrator** roles
- [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- Access to [Microsoft Foundry](https://ai.azure.com)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/foundry-agents-essentials.git
cd foundry-agents-essentials
```

### 2. Deploy to Azure

```bash
azd auth login
azd up
```

This provisions all Azure resources (App Service, Foundry, Grounding with Bing, Azure AI Search) and deploys the onboarding tracker application.

> **Note:** The deployment automatically grants the deployer the **Azure AI User** role on the Foundry resource. If a different user needs Foundry access, pass their principal ID during deployment:
> ```bash
> azd up --parameter foundryUserPrincipalId=<USER_OBJECT_ID>
> ```

### 3. Start the lab

Open [Unit 1](docs/unit-1-declarative-agent.md) and follow along!

## Architecture

```
┌──────────────────────────────────────────────────┐
│              Foundry Agent                        │
│       (created by student in portal)              │
└───────┬─────────────┬────────────────────────────┘
        │             │
  Grounding      MCP (Streamable HTTP)
  with Bing           │
                      ▼
          ┌───────────────────────┐
          │   Python Backend      │
          │   (Azure App Service) │
          │                       │
          │  ┌─────────────────┐  │
          │  │  MCP Server     │  │
          │  │  /mcp           │  │
          │  └─────────────────┘  │
          │  ┌─────────────────┐  │
          │  │  REST API       │  │
          │  │  /api/onboarding│  │
          │  └─────────────────┘  │
          │  ┌─────────────────┐  │
          │  │  React Frontend │  │
          │  │  (static files) │  │
          │  └─────────────────┘  │
          └───────────────────────┘
```

## Project Structure

```
foundry-agents-essentials/
├── azure.yaml              # Azure Developer CLI project config
├── infra/                  # Bicep infrastructure-as-code
├── src/app/
│   ├── backend/            # Python FastAPI + MCP server
│   └── frontend/           # React onboarding tracker UI
└── docs/                   # Lab unit guides
    └── sample-documents/   # Sample firm documents for lab exercises
```

## Local Development

Run the backend and frontend in **separate terminals**. The Vite dev server proxies `/api` and `/mcp` requests to the backend automatically.

### Backend

```bash
cd src/app/backend
python -m venv .venv
.venv\Scripts\activate      # On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd src/app/frontend
npm install
npm run dev
```

> Open the Vite URL (default `http://localhost:5173`). API calls are proxied to the backend at `http://localhost:8000`.

## MCP Tools Reference

The onboarding MCP server (at `/mcp`) exposes these tools:

| Tool | Description |
|------|-------------|
| `list_onboardings` | List all client onboardings with their current status |
| `get_onboarding` | Get details of a specific onboarding by ID |
| `create_onboarding` | Create a new client onboarding record |
| `update_status` | Update the status of an onboarding (e.g., pending → in-review → approved) |
| `add_note` | Add a note or comment to an onboarding record |

## Sample Documents

The `docs/sample-documents/` folder contains files used during the lab exercises:

| Document | Used In | Description |
|----------|---------|-------------|
| `firm-onboarding-handbook.md` | Unit 3 | Firm policies and procedures for client onboarding |
| `sample-proposal.md` | Unit 6 | A sample client proposal for field extraction exercises |

## Redeployment

After making code changes, redeploy with:

```bash
azd deploy
```
