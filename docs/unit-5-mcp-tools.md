# Unit 5: MCP Tools & Actions

## Overview

Welcome to Unit 5 of the **Foundry Agents Essentials** workshop — and the moment everything comes together! Over the past four units, you've built an increasingly capable agent: it has a professional persona (Unit 1), can search the web (Unit 2), knows your firm's policies (Unit 3), and has polished instructions with scope boundaries, conversational flow patterns, and a structured intake workflow (Unit 4). But so far, your agent has only been able to *talk* — it generates text, answers questions, and walks users through processes, yet it can't actually *do* anything in the real world.

That changes now. In this unit, you'll connect your onboarding-agent to a **live client onboarding tracker** application using the **Model Context Protocol (MCP)**. Once connected, the agent will be able to create new client onboarding records, update matter statuses, and add compliance notes — all by calling real API endpoints on a running application. You'll watch the agent take an action in the Foundry playground and then see the result appear in a live web dashboard, in real time.

For legal firms, this is where AI agents translate intelligence into action across legal workflows. Imagine your agent completing a guided intake conversation (Unit 4), then automatically creating the matter record in your practice management system, flagging it for conflicts review, and logging a compliance note — all without anyone copying and pasting between systems. By the end of this unit, you'll see exactly how that works. And as always, you won't write a single line of code.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Completed [Unit 4: Crafting Instructions & Conversational Flow](./unit-4-instructions-and-flow.md)
- ✅ Your **onboarding-agent** is working in the Foundry playground with all prior capabilities configured (Bing grounding, file-based knowledge grounding, structured intake instructions)
- ✅ Infrastructure deployed via `azd up` (this deploys the onboarding tracker web app to Azure App Service)
- ✅ The onboarding tracker web app is running and accessible (you'll find the URL in the Azure Portal)
- ✅ Access to the [Microsoft Foundry portal](https://ai.azure.com)

> **📝 Note:** You can find your web app URL in the [Azure Portal](https://portal.azure.com): navigate to your resource group → select the **App Service** resource → on the Overview page, the URL is shown under **Default domain** (e.g., `https://app-xxxx.azurewebsites.net`).

---

## What is MCP?

Before we connect anything, let's understand what MCP is and why it matters.

**Model Context Protocol (MCP)** is an open standard that defines how AI agents communicate with external tools and services. Think of it as **USB-C for AI** — before USB-C, every device had its own proprietary charger and cable. You needed a different connector for your phone, tablet, laptop, and headphones. USB-C solved that by providing one universal standard. MCP does the same thing for AI agents: instead of building custom integrations for every tool, you build one MCP server and any MCP-compatible agent can connect to it.

Here's how it works in practice:

1. **MCP Server** — A service exposes a set of tools, each with a name, a description, and an input schema. The server says: "Here are the things I can do and the information I need to do them."
2. **Tool Discovery** — When you connect an agent to an MCP server, the agent automatically discovers all available tools. It reads their names, descriptions, and schemas — no manual configuration of individual tools required.
3. **Agent Decides** — When a user sends a message, the agent reads the tool descriptions and decides on its own whether (and which) tools to call. You don't write any routing logic.
4. **Streamable HTTP Transport** — The agent communicates with the MCP server over standard HTTPS. In our case, the onboarding tracker exposes its MCP endpoint at `/mcp`, and Foundry calls it using the Streamable HTTP transport — simple, secure, and firewall-friendly.

### Read vs. Write Operations

A critical distinction in MCP tools is whether they **read** data or **write** (change) data:

- **Read tools** are safe and idempotent — calling them doesn't change anything. You can call them as many times as you want without side effects.
- **Write tools** change state in the target system — creating records, updating statuses, or adding data. These are the tools that make your agent capable of real action.

Your onboarding tracker MCP server exposes five tools:

| Tool | Type | Description |
|------|------|-------------|
| `list_onboardings` | Read | List all client onboardings with status, client name, and engagement type |
| `get_onboarding` | Read | Get full details of a specific onboarding by ID (e.g., OB-001) |
| `create_onboarding` | Write | Create a new client onboarding record (client name, engagement type, description, contact email) |
| `update_status` | Write | Update an onboarding's status (pending, in-review, approved, active, completed, on-hold) |
| `add_note` | Write | Add a note or comment to an onboarding record |

> **💡 Tip:** You don't need to tell the agent when to use each tool. The agent reads the tool descriptions and decides on its own. If a user asks "show me all onboardings," the agent will call `list_onboardings`. If a user says "create a new matter for Contoso," the agent will call `create_onboarding`. This is the power of well-described MCP tools.

### Why MCP Matters for Legal Firms

The pattern you're about to see — connecting an agent to a backend system via MCP — is the same pattern you'd use to connect to practice management systems, document management, billing platforms, or any other system your firm relies on. MCP provides the universal adapter. Build one MCP server for each system, and your agents can interact with all of them.

---

## Steps

### Step 1: Open the Onboarding Tracker

Before connecting the agent, let's see the application it will be interacting with.

1. Find your web app URL in the [Azure Portal](https://portal.azure.com):
   - Navigate to your **resource group**
   - Select the **App Service** resource
   - On the **Overview** page, copy the URL shown under **Default domain** (e.g., `https://app-xxxx.azurewebsites.net`)

2. Open the URL in your browser. You should see the **Client Onboarding Tracker** — a React dashboard with:
   - **Status cards** at the top showing counts by status (pending, in-review, approved, etc.)
   - **A list of onboarding records** in the main area
   - **Three seeded sample records** already in the system

3. Review the seeded records:

   | ID | Client | Engagement Type | Status |
   |----|--------|----------------|--------|
   | OB-001 | MCO | Regulatory Compliance | In Review |
   | OB-002 | Adatum Corporation | Litigation | Approved |
   | OB-003 | Northwind Traders Inc | Corporate & Transactions | Pending |

4. Click on any record to see its **detail view**, including the full description, contact information, timestamps, and any notes attached to the record.

5. Take a moment to appreciate what's running here — a **Python FastAPI backend** serving a **React frontend**, with an **MCP server** at `/mcp`, all deployed automatically by `azd up`. The infrastructure templates handled everything.

> **📝 Note:** The tracker dashboard polls for updates every 3 seconds. This means when your agent creates or updates a record, you'll see the change appear in the dashboard almost immediately — no manual refresh required.

> **💡 Tip:** Keep this browser tab open! You'll want it side-by-side with the Foundry playground so you can watch the real-time feedback loop as your agent takes actions.

---

### Step 2: Add the MCP Connection to Your Agent

Now let's connect your onboarding-agent to the tracker's MCP server.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) and navigate to your **onboarding-lab** project.
2. In the top navigation bar, select **Build**. In the left-hand navigation, click on **Agents**.
3. Select the **onboarding-agent** to open its configuration.
4. Scroll down to the **Tools** section. You should already see **Grounding with Bing Search** listed from Unit 2.
5. Click **Add** to add a new tool.
6. Select **Custom** and then **MCP**.
7. Configure the MCP connection:
   - **Server URL:** `https://app-xxxx.azurewebsites.net/mcp` — replace with your actual App Service URL from the Azure Portal, appending `/mcp`
   - **Authentication:** Unauthenticated
   - **Name:** `onboarding-tracker`
8. Click **Connect**. Foundry will register the MCP server connection. The agent discovers tools at runtime — you may not see individual tools listed in the configuration UI.
9. Click **Save** to save your agent configuration.

> **📝 Note:** Your agent now has multiple tool sources — **Bing** for web search and the **Onboarding Tracker** for matter management. The agent will choose the right tool based on the question. Ask about current regulations? It uses Bing. Ask about client onboardings? It uses the tracker. Ask about firm policies? It uses the uploaded documents. The agent handles this routing automatically.

> **💡 Troubleshooting:** If the agent can't reach the MCP server during testing:
> - Verify your web app is **running** — go to the Azure portal → your App Service → Overview and check the status is "Running."
> - Confirm the URL format: `https://app-xxxx.azurewebsites.net/mcp` (the `/mcp` path is required).
> - The MCP endpoint is designed for agent-to-agent communication, not browser access — visiting the URL directly in a browser may return an error or blank page. This is normal.
> - If the app was just deployed, give it a minute to start up (cold start).

---

### Step 3: Test Read Operations (and Verify the Connection)

Let's start with read-only operations to confirm the MCP connection is working. These are safe — they don't change any data. **This is also how you verify that tools were discovered correctly.**

1. In the Foundry portal, open the **playground** for your onboarding-agent.
2. Try listing all onboardings:

   ```
   Show me all current client onboardings.
   ```

   The agent should call `list_onboardings` and display all three seeded records with their client names, engagement types, and statuses. This is **real data** coming from the running application — not a canned response. **If you see real onboarding data, the MCP connection is working.**

   > **📝 Note:** The five tools your MCP server exposes are: `list_onboardings`, `get_onboarding`, `create_onboarding`, `update_status`, and `add_note`. You'll exercise all of them in this unit.

3. Now get details on a specific matter:

   ```
   What's the details and status of the MCO matter?
   ```

   The agent should call `get_onboarding` for OB-001 and return the full details — including the description, contact email, timestamps, and current status (in-review).

4. Try a question that requires the agent to filter results:

   ```
   Which matters are currently pending?
   ```

   The agent should call `list_onboardings` and identify that Northwind Traders Inc (OB-003) is the only matter with a "pending" status.

5. Try one more to see how the agent handles a lookup by context rather than ID:

   ```
   Give me the details on the Adatum litigation matter.
   ```

   The agent should find OB-002 and return its full details, including the "approved" status.

> **📝 Note:** The agent is reading **live data** from your onboarding tracker application. If someone else modifies a record in the app, the agent's next read will reflect those changes. This is a real, connected system — not a simulation.

---

### Step 4: Test Write Operations

Now for the exciting part — let's have the agent **change state** in the tracker application. Arrange your screen so you can see the **Foundry playground** and the **tracker dashboard** side by side.

1. **Create a new onboarding record.** In the Foundry playground, send:

   ```
   Create a new onboarding for Trey Research. It's an employment law matter — workplace discrimination case involving allegations of wrongful termination. The firm will handle the investigation and defense. Contact is Sarah Chen at sarah@treyresearch.com.
   ```

   The agent will follow the structured intake flow from Unit 4 — it may ask follow-up questions to gather additional details like engagement value, urgency level, and referral source before creating the record. This is the multi-step intake process working as designed. Provide the requested information and the agent will proceed.

   Once it has all the details, it will call `create_onboarding` via the MCP server. Now **look at the tracker dashboard** — a new record should appear within a few seconds! You'll see "Trey Research" in the list with a "pending" status.

   > **💡 Tip:** This is Unit 4 and Unit 5 working together — the **instructions** guide the agent to collect complete intake information, and the **MCP tools** let it create the actual record. The agent doesn't just dump data into the tracker blindly; it follows your firm's intake process first.

2. **Update a matter's status.** Try:

   ```
   Update the MCO matter to active status.
   ```

   The agent should call `update_status` for OB-001. If anything needs to be completed before moving to Active, the agent flow will ask user for confirmation. Watch the tracker dashboard — the MCO status badge should change from "In Review" to "Active."

3. **Add a note to a matter.** Try:

   ```
   Add a note to the Adatum matter: "Engagement letter countersigned by client. Ready to proceed with discovery."
   ```

   The agent should call `add_note` for OB-002. Click on the Adatum Corporation record in the tracker dashboard and check the detail view — your note should appear in the notes section.

4. **Verify the changes persisted.** Ask the agent:

   ```
   Show me all onboardings again.
   ```

   You should now see **four records** (the original three plus Trey Research), with MCO showing "active" status.

> **💡 Tip:** This real-time feedback loop is the key insight of this unit — the agent takes an action in the Foundry playground, the MCP server processes it, the tracker's state changes, and the React dashboard updates automatically. Agent acts → app state changes → user sees the result. This is what makes MCP-connected agents genuinely useful.

> **📝 Note:** Every action the agent takes through MCP is a real API call to a real backend. The records it creates are stored in the application's database. This is production-grade integration, not a demo trick.

---

### Step 5: Full End-to-End Workflow

This is the capstone of the entire workshop. You'll run a **complete guided intake conversation** — using the structured flow you configured in Unit 4 — that ends with the agent **creating a real onboarding record** in the tracker.

1. Start a **new conversation** in the Foundry playground (click the new chat button to clear history). Then send:

   ```
   I need to onboard a new client.
   ```

   The agent should begin the structured intake flow from Unit 4, asking you for the matter type first.

2. Provide the matter type:

   ```
   It's an intellectual property matter — patent filing for a new technology product.
   ```

3. Provide client details when the agent asks:

   ```
   The client is Fourth Coffee. Primary contact is Alex Rivera at alex@fourthcoffee.com. Fourth Coffee is developing a new automated brewing system and needs patent protection for the core technology before their product launch. Estimated engagement value is $40,000, standard urgency.
   ```

4. Continue through the intake flow. The agent should walk you through:
   - Confirming the engagement type and scope
   - Asking about required documents (engagement letter, NDA, etc.)
   - Checking whether conflicts screening has been initiated
   - Summarizing all gathered information

5. When the agent presents the summary and asks if you'd like to proceed, confirm:

   ```
   Yes, please create the onboarding record.
   ```

   The agent should call `create_onboarding` with all the information gathered during the conversation — client name, engagement type, description, and contact email. **Watch the tracker dashboard** — the Fourth Coffee record should appear!

6. Verify the record was created correctly:

   ```
   Show me the full details of the Fourth Coffee onboarding.
   ```

   The agent should call `get_onboarding` and display the complete record, confirming that all the details from the intake conversation were captured accurately.

7. Check the tracker dashboard one more time. You should now see **five records** — the three original seeded records, the Trey Research record from Step 4, and the new Fourth Coffee record from this workflow.

> **💡 Tip:** This end-to-end flow demonstrates the full agent lifecycle: **knowledge** (the agent knows firm policies from the handbook) + **instructions** (the agent follows a structured intake process) + **tools** (the agent creates real records via MCP) = a complete, automated workflow. This is what production-ready AI agents look like.

> **📝 Note:** The agent may word things slightly differently each time you run through this flow — that's the nature of language models. Structured instructions improve consistency, but for scenarios where you need **guaranteed step sequences and deterministic flow control**, you'll use Workflow Agents in Unit 6.

---

### Step 6: Combine All Capabilities

Your agent now has four distinct capabilities: web search (Bing), firm knowledge (file uploads), structured conversational flow (instructions), and real actions (MCP tools). Let's see them work together seamlessly in a single conversation.

1. Try a prompt that exercises **web search and matter management** together:

   ```
   I need to onboard Relecloud as a new regulatory compliance client. Before we start, can you check if there are any recent changes to FDA compliance regulations that might be relevant?
   ```

   Watch how the agent uses **Bing** to research current FDA regulations *and* then offers to create the onboarding record using the **MCP tools** — multiple capabilities in one natural conversation.

2. Now try a prompt that combines **firm knowledge and matter data**:

   ```
   What approval level does the Fourth Coffee matter need based on our firm's policies?
   ```

   The agent should use the **uploaded firm documents** to look up the approval thresholds from the firm handbook ($25,000–$100,000 requires Practice Director approval) and apply that to the Fourth Coffee engagement's $40,000 estimated value.

3. Try one more that pulls everything together:

   ```
   Add a note to the Fourth Coffee onboarding: "Conflicts check completed — no conflicts identified. Engagement letter sent to client for signature." Then tell me what the next steps should be according to our onboarding procedures.
   ```

   The agent should call `add_note` via **MCP**, then reference the **uploaded documents** to describe the next steps in the onboarding lifecycle.

> **💡 Tip:** This is the real power of declarative agents in Foundry. Each capability you added in Units 1–5 is still active and working. The agent doesn't just use one tool at a time — it blends web knowledge (Bing), firm knowledge (uploaded documents), structured behavior (instructions), and real actions (MCP) together seamlessly, choosing the right capability for each part of the conversation.

---

## Summary

🎉 **Congratulations — you've built a complete, working AI agent!** Starting from a blank canvas in Unit 1, you've progressively built an agent that understands your firm's policies, searches the web for current information, guides users through structured workflows, and takes real actions in a live application. That's a production-grade legal AI assistant, built entirely through portal configuration.

| Unit | What You Added | Capability |
|------|---------------|------------|
| **Unit 1** | Declarative agent + instructions | Agent has a persona and can chat |
| **Unit 2** | Grounding with Bing | Agent searches the web for current information |
| **Unit 3** | File-based knowledge grounding | Agent answers from uploaded documents with citations |
| **Unit 4** | Structured instructions + conversational flow | Agent has scope boundaries, consistent personality, conversational patterns, and a structured intake workflow |
| **Unit 5** | MCP tools + onboarding tracker | Agent creates records, updates status, and takes real actions |

### Key Takeaway

MCP transforms your agent from a **conversational assistant** into a **workflow automation tool**. Without MCP, the agent can talk about onboarding but can't actually do it. With MCP, the agent completes the entire process — gathering information, applying firm policies, and creating the record in your system. For legal firms, this is the pattern that unlocks real productivity gains: the same MCP approach connects to practice management systems, document management platforms, billing software, court filing systems, and any other tool your firm uses. The protocol is open, the integration is standardized, and the agent handles the orchestration.


### When One Agent Isn't Enough — Multi-Agent Orchestration

In this unit, a single prompt agent handles everything: it collects intake details, checks policies, and creates the record. That works well for straightforward scenarios, but as your firm's use cases grow, you may want **multiple specialized agents** working together — an intake specialist, a research analyst, a compliance reviewer, each with their own instructions and tools.

There are two ways to coordinate multiple agents:

| Approach | How it works | Built in portal? |
|----------|-------------|-----------------|
| **Workflow agents** | You define the exact sequence — Agent A runs, then Agent B, then Agent C. You control the flow. | ✅ Yes — visual builder, no code |
| **Agentic orchestration** | A "manager" agent dynamically decides which specialist agents to call based on the conversation. The AI controls the routing. | ❌ No — requires pro-code |

You'll build a workflow agent in **[Unit 6](./unit-6-workflow-agents.md)** using the portal's visual builder — no code needed. But if your firm needs dynamic agent-to-agent delegation (e.g., a triage agent that routes inquiries to the right practice group's specialist agent based on matter type), that's where you'd move to pro-code using an orchestration framework like the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) SDKs available for Python and .NET, or other multi-agent orchestration framework. 

> **💡 Foundry + Microsoft Agent Framework:** Foundry agents are designed to integrate seamlessly with the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). You can deploy agents built in the Foundry portal as hosted endpoints, then use the Agent Framework to orchestrate them alongside code-first agents in Python or .NET. This gives you the best of both worlds — rapid prototyping in the portal for individual agents, and the Agent Framework for production-grade multi-agent coordination with features like state management, event-driven routing, and agent-to-agent communication.

### What's Next

In **[Unit 6: Workflow Agents](./unit-6-workflow-agents.md)**, we'll move from single-prompt agents to multi-step pipelines with human approval. You'll build a workflow agent that coordinates sequential tasks with controlled flow — no code needed.

---

## Key Concepts

- **Model Context Protocol (MCP)** — An open standard that defines how AI agents communicate with external tools and services. Like USB-C for AI — any MCP-compatible agent can connect to any MCP server without custom integration code.

- **MCP Server** — A service that exposes tools to AI agents via MCP. Each tool has a name, description, and input schema. In this unit, the onboarding tracker's FastAPI backend serves as the MCP server at `/mcp`.

- **Streamable HTTP** — The transport protocol used by MCP over standard HTTPS, making it firewall-friendly and compatible with standard web infrastructure.

- **Tool Discovery** — The agent automatically detects available tools on an MCP server by reading the server's tool catalog — no manual configuration needed.

- **Read vs. Write Operations** — Read tools (like `list_onboardings`) retrieve data safely. Write tools (like `create_onboarding`) modify state and represent real actions with real consequences.

- **Agent Tool Chaining** — When an agent calls multiple tools in sequence within a single conversation — e.g., creating a record, adding a note, then confirming the result.

> **💡 Tip:** The MCP ecosystem is growing rapidly. Visit [modelcontextprotocol.io](https://modelcontextprotocol.io) to explore available servers, community tools, and the full protocol specification.
