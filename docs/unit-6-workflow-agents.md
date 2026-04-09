# Unit 6: Workflow Agents

## Overview

Welcome to Unit 6 of the **Foundry Agents Essentials** workshop! Up to this point, every agent you've built has been a **prompt agent** — a single agent that receives a user message, reasons about what to do, and responds. Prompt agents excel at open-ended conversations, flexible problem-solving, and tasks where the user drives the interaction.

But some tasks aren't conversations — they're **processes**. For legal firms, client intake has mandatory steps that must happen in a specific order, every time, for every client. A conflicts check must complete before an engagement letter is drafted. A partner must approve before the matter becomes active. These aren't suggestions — they're requirements.

**Workflow agents** give you a different tool for this different purpose. Instead of giving one agent all the tools and relying on it to follow the right sequence, you build a **workflow** — a visual, step-by-step pipeline where **you define the exact order of operations**. Each step runs a specialized agent (or a logic block, or a human approval gate), and the next step doesn't start until the previous one completes. The AI still powers the intelligence within each step, but **you control the flow between steps**.

This is an important architectural concept in the workshop: prompt agents for flexibility, workflow agents for control.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Infrastructure deployed via `azd up`
- ✅ Access to the [Microsoft Foundry portal](https://ai.azure.com)

> **📝 Note:** This unit introduces the **Workflows** feature in Microsoft Foundry. Workflows are created and managed through the Foundry portal — no code, no YAML, no SDK. You'll use the visual workflow builder to design, connect, and test your multi-step pipeline.

---

## Prompt Agents vs. Workflow Agents

Before we build anything, let's understand *why* workflow agents exist and when you need them.

### When You Need Defined Processes

Over the past five units, you've built a highly capable prompt agent. It can:

- Research a prospective client using Bing (Unit 2)
- Look up firm policies from uploaded documents (Unit 3)
- Guide the user through a structured intake conversation (Unit 4)
- Create onboarding records via MCP tools (Unit 5)

That's impressive. But when a user says "I need to onboard Contoso Ltd as a new client," the agent decides on its own which of those capabilities to use and in what order. That flexibility is great for open-ended interactions, but for a **defined process** with mandatory steps, you want something more structured.

### What Legal Firms Actually Need

Legal client intake follows a defined process — the five-stage onboarding lifecycle from your [firm handbook](./assets/firm-onboarding-handbook.md):

| Stage | What Happens | Can It Be Skipped? |
|-------|-------------|-------------------|
| **1. Intake** | Collect client details, matter type, scope | ❌ Never |
| **2. Due Diligence** | Research the client, check for conflicts | ❌ Never |
| **3. Scope & Proposal** | Summarize the engagement for partner review | ❌ Never |
| **4. Approval** | Partner reviews and approves | ❌ Never |
| **5. Activation** | Create the matter record in the system | ❌ Never |

Every step must happen. Every step must happen in order. A prompt agent is flexible by design — it adapts to the conversation. A workflow agent is **deterministic by design** — you build the sequence yourself, and it runs the same way every time.

### The Key Difference

| | Prompt Agent | Workflow Agent |
|---|---|---|
| **Who controls the flow?** | The AI decides which tools to call and in what order | You define the exact sequence of steps |
| **Step sequence** | Flexible — adapts to the conversation | Fixed — every step runs, in order |
| **Consistency** | Adaptive per conversation | Same process every time |
| **Human approval** | Not a built-in concept | Built in — workflow pauses at approval gates |
| **Auditability** | Hard to verify what happened | Each step logs its input and output |
| **Best for** | Open-ended Q&A, research, exploration | Defined processes with mandatory steps |

> **💡 Tip:** Prompt agents and workflow agents aren't competing approaches — they're complementary. In this unit, you'll build a workflow that *uses* prompt agents as steps. The workflow controls the sequence; the prompt agents handle the intelligence within each step. Think of it as: **the workflow is the process; the agents are the workers.**

### What About Multi-Agent Orchestration?

There's a third pattern: **agentic orchestration** — where a "manager" agent dynamically routes tasks between specialist agents. That pattern requires pro-code using an orchestration framework like the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). For legal intake — a defined process with mandatory steps — **workflow agents are the right fit**. Everything you build in the portal carries forward if you move to pro-code later.

---

## The Workflow You'll Build

Here's the client intake workflow you'll create in this unit. It follows the firm's onboarding lifecycle and ensures every step happens, in order, every time:

```
┌─────────────────────────────────────────────────────────┐
│                    INTAKE WORKFLOW                       │
│                                                         │
│  ┌───────────────┐                                      │
│  │  Step 1       │  Intake Agent collects client        │
│  │  INTAKE       │  details through conversation        │
│  └───────┬───────┘                                      │
│          │ client details passed as variables            │
│          ▼                                              │
│  ┌───────────────┐                                      │
│  │  Step 2       │  Research Agent searches Bing        │
│  │  DUE DILIGENCE│  for client background & risks       │
│  └───────┬───────┘                                      │
│          │ research findings passed forward              │
│          ▼                                              │
│  ┌───────────────┐                                      │
│  │  Step 3       │  Review Agent checks firm policies   │
│  │  COMPLIANCE   │  and generates partner brief         │
│  └───────┬───────┘                                      │
│          │ summary + recommendation passed forward       │
│          ▼                                              │
│  ┌───────────────┐                                      │
│  │  Step 4       │  Human reviews the summary and       │
│  │  APPROVAL     │  approves or rejects                 │
│  └───────┬───────┘                                      │
│          │ approval decision passed forward              │
│          ▼                                              │
│  ┌───────────────┐                                      │
│  │  Step 5       │  Activation Agent creates the        │
│  │  ACTIVATION   │  onboarding record via MCP           │
│  └───────────────┘                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

Notice something important: **no single agent does everything**. Each step has a specialized agent with a focused role. The Intake Agent only collects details. The Research Agent only searches. The Review Agent only checks policies. The workflow coordinates them — passing data between steps and enforcing the sequence.

This is the fundamental shift: **you are the architect of the process, not the AI.**

---

## Steps

### Step 1: Navigate to the Workflow Builder

Let's start by opening the workflow builder in the Foundry portal.

1. Go to the [Microsoft Foundry portal](https://ai.azure.com) and open your **onboarding-lab** project
2. On the upper-right menu, select **Build**, then select **Agents** on the left menu, and then select the **Workflows** tab under Agents.
3. Click **Create workflow**. You'll see workflow template options. Select **Sequential** — this creates a linear, step-by-step workflow where each step runs after the previous one completes. You should now see the Visualizer display of the workflow with three agent cards and a sequential flow created with Start and the Agent cards.
4. Click **+** between the Start and the first Agent card to add a new step **Set variable**. Select **Set Variable** node, and select **Edit** and configure variables that the workflow will use to pass data between steps. Add the following variables with leaving **To value** as is for now (you'll set them in the agent steps later):
   - `Local.intake_details` — The structured output from Step 1 (client name, matter type, scope, etc.)
   - `Local.research_brief` — The due diligence findings from Step 2
   - `Local.compliance_summary` — The review outcome and executive summary from Step 3
   - `Local.approval_decision` — The partner's approve/reject decision from Step 4
5. Click **Done** to save the variable configuration and return to the canvas. You should now see the Start → Set Variable → Agent flow on the canvas.
6. Delete the sticky notes and Click **Save** and give your workflow a name: `client-intake-workflow`

> **📝 Note:** The sequential template is the right choice for client intake because every step depends on the previous step's output. Foundry also offers **Group Chat** workflows (multiple agents collaborate in a conversation) and **Human-in-the-loop** templates. You'll add a human approval step within the sequential flow.

---

### Step 2: Create the Intake Agent (Step 1 of the Workflow)

The first step in the workflow collects client details. You'll create a specialized prompt agent for this — simpler and more focused than your all-in-one onboarding-agent.

1. Select the first **Agent** card on the workflow canvas or Add another **Agent** step to the workflow canvas if missing (click **+** after the Set variables step), 
2. Select **Edit** from the menu, Agent Builder will open.
3. In the **Select an agent** drop down, select **Create a new agent**, Name it: `intake-collector`
4. Set the model to your deployed model (e.g., `gpt-4.1`)
5. Under the **Input** section, make sure the agent's input is mapped to the workflow trigger's user message (e.g., `${trigger.input}` or the start node's output variable). If this mapping is missing or points to an empty variable, the agent will fail with an `InvokeAzureAgent` error.
5. Add the following instructions:

```
## Role
You are the intake collector for Meridian Legal's onboarding workflow. Gather all required details for a new client engagement through a brief, focused conversation.

## Scope
ONLY collect intake information. Do not research the client, check firm policies, or create any records — those happen in later workflow steps.

## Required Fields
Collect each of the following. Ask one or two questions at a time:
1. Client name (legal entity or individual)
2. Primary contact name and email
3. Matter type (Legal Advisory, Litigation, Corporate & Transactions, Regulatory Compliance, Employment Law, or Intellectual Property)
4. Brief description of the engagement scope (2–3 sentences)
5. Estimated engagement value
6. Any known prior relationships or potential conflicts with this client

## Output Format
Once all fields are collected, output a structured summary in this exact format:

CLIENT: [name]
CONTACT: [name, email]
MATTER TYPE: [type]
SCOPE: [description]
ESTIMATED VALUE: [value or "Not provided"]
PRIOR RELATIONSHIP: [yes/no and details]
```

6. Do not add any tools (Bing, knowledge bases, or MCP) to this agent — it only needs to collect information through conversation
7. Still in **Node settings**, select the **Save agent output message as** and select `Local.intake_details` (this is how the workflow will pass the collected information to the next step)
8. Click **Done** to save the agent and return to the workflow canvas

Notice how different these instructions are from the all-in-one onboarding-agent. This agent has one job. It can't research, it can't check policies, it can't create records. That's not a limitation — it's the whole point. **Each agent in a workflow does one thing well. The workflow handles the rest.**

> **💡 Tip:** The structured output format (CLIENT, CONTACT, MATTER TYPE, etc.) isn't arbitrary — it makes it easy for the next step in the workflow to parse and use the information. When designing workflow agents, think about how each step's output becomes the next step's input.

---

### Step 3: Create the Research Agent (Step 2 of the Workflow)

The second step researches the client for background, recent news, and potential risks. This is the due diligence step of the onboarding lifecycle.

1. Select the second **Agent** card on the workflow canvas or Add another **Agent** step to the workflow canvas if missing (click **+** after the intake-collector step). 
2. Select **Edit** from the menu, Agent Builder will open.
3. In the **Select an agent** drop down, select **Create a new agent**, Name it: `client-researcher`
4. Set the model to your deployed model (e.g., `gpt-4.1`)
5. Add the following instructions:

```
## Role
You are the due diligence researcher for Meridian Legal's onboarding workflow. You receive intake details from the previous step and research the prospective client.

## Scope
ONLY perform client research using web search. Do not check firm policies, make engagement recommendations, or create any records.

## Tasks
Using the client name and matter details provided:
1. Search for the client's background — what they do, size, and industry
2. Find recent news, press releases, or significant developments
3. Identify any regulatory actions, lawsuits, or legal issues involving the client
4. Assess reputational risk based on your findings

## Output Format
COMPANY OVERVIEW: [2–3 sentences]
RECENT DEVELOPMENTS: [bullet points of relevant news, or "None found"]
LEGAL/REGULATORY HISTORY: [known issues, or "No issues found"]
RISK ASSESSMENT: [Low / Medium / High — with brief justification]

## Example
If you find no concerning information:
RISK ASSESSMENT: Low — No regulatory actions, lawsuits, or negative press identified. Client appears to be an established company with a clean public record.
```

6. Add **Bing Grounding** as a tool for this agent — it needs web search to do its job
7. Do NOT add knowledge bases or MCP tools
8. Select the **Node settings** tab in the Agent Builder, select the **Input message as** and select `Local.intake_details` and select the **Save agent output message as** and select `Local.research_brief`(this is how the workflow will pass the collected information to the next step)
9. Click **Done** to save the agent and return to the workflow canvas

**This is the power of workflows**: the Research Agent has Bing grounding, but the Intake Agent doesn't. Each agent gets exactly the tools it needs — nothing more. In a prompt agent approach, one agent has all the tools and the AI decides which to use. In a workflow, **you decide which tools each step can access.**

---

### Step 4: Create the Compliance Review Agent (Step 3 of the Workflow)

The third step checks the intake against firm policies and generates a partner-ready summary. This is where the knowledge from Unit 3 comes in.

1. Select the third **Agent** card on the workflow canvas or Add another **Agent** step to the workflow canvas if missing (click **+** after the client-researcher step). 
2. Select **Edit** from the menu, Agent Builder will open.
3. In the **Select an agent** drop down, select **Create a new agent**, Name it: `compliance-reviewer`
4. Set the model to your deployed model (e.g., `gpt-4.1`)
5. Add the following instructions:

```
## Role
You are the compliance reviewer for Meridian Legal's onboarding workflow. You receive the intake details and research brief from previous steps. Your job is to check everything against firm policies and prepare a summary for partner approval.

## Scope
ONLY review compliance and prepare the summary. Do not approve the engagement (that is the partner's decision) and do not create any records.

## Tasks
1. Check the engagement against the firm's onboarding handbook:
   - Does the matter type match a recognized practice area?
   - Is the estimated value above the minimum engagement threshold?
   - Are all required intake fields complete?
2. Determine the required approval level based on engagement value:
   - Under $25,000 → Engagement Lead
   - $25,000–$100,000 → Practice Director
   - $100,000–$500,000 → Managing Partner
   - Over $500,000 → Executive Committee
3. Flag any compliance concerns (prior relationships, regulatory sensitivity, missing information)
4. Write a concise executive summary for the approving partner

## Output Format
COMPLIANCE STATUS: [Pass / Needs Review / Fail]
ISSUES FOUND: [list issues, or "None"]
APPROVAL LEVEL REQUIRED: [Practice Director / Managing Partner / Executive Committee]
EXECUTIVE SUMMARY: [3–4 sentences covering who the client is, what they need, research highlights, and any concerns]
```

6. Under **Tools** section, click **Upload Files**, upload documents under assets folder (the firm documents you uploaded in Unit 3)
7. Do NOT add Bing or MCP tools
8. Select the **Node settings** tab in the Agent Builder, select the **Input message as** and select `Local.research_brief` and select the **Save agent output message as** and select `Local.compliance_summary`(this is how the workflow will pass the collected information to the next step)
9. Click **Done** to save the agent and return to the workflow canvas

Again, this agent has exactly one capability: checking firm policies via the knowledge base. It can't search the web (that already happened in Step 2) and it can't create records (that happens in Step 5). **The workflow ensures each step stays in its lane.**

---

### Step 5: Add a Human Approval Gate (Step 4 of the Workflow)

This is the step that highlights a key workflow advantage. The workflow **pauses** and waits for a human to review the summary and make a decision — something that's natural in a workflow but not built into a prompt agent's conversation model.

1. Add a **Ask a question** step to the workflow canvas (this is a built-in step type, not an agent)
2. Configure the step:
   - **Question** Display the compliance-reviewer's output (the executive summary, compliance status, and any flagged issues) and ask the partner to approve or reject. For example: The client intake compliance summary:
{Local.compliance_summary} Please provide approval and optional comments- Approved, or Rejected.
   - **Save user response as** Local.approval_decision
3. Click **Done** to save and return to the canvas

When the workflow reaches this step, it **stops and waits**. No timer, no timeout, no AI making the decision. A real person — the approving partner — reviews the executive summary from Step 3, sees the research findings from Step 2, and makes a judgment call. Only when they respond does the workflow continue.

**This is a key reason workflows exist for legal firms.** No matter how good the AI is at research, policy checking, and summarization, the approval decision must be made by a human. Workflows make this a first-class concept — the process pauses, waits for a real person to review and decide, and only then continues.

> **📝 Note:** In a production deployment, you'd configure notifications (email or Teams) to alert the reviewing partner when an approval is waiting. For this workshop, you'll trigger the approval manually during testing.

---

### Step 6: Create the Activation Agent (Step 5 of the Workflow)

The final step creates the onboarding record in the tracker — but only if the partner approved.

1. Add another **Agent** step to the workflow canvas, after the human approval step. Select **Edit** from the menu, Agent Builder will open.
2. Create a new agent named: `record-creator`
3. Set the model to your deployed model
4. Add the following instructions:

```
## Role
You are the record activation agent for Meridian Legal's onboarding workflow. You receive the approved intake details and create the official onboarding record in the tracker system.

## Scope
ONLY create records and add notes. Do not perform research or review compliance — those steps are already complete.

## Tasks
1. Check the approval decision from the previous step
2. If APPROVED:
   - Use create_onboarding with the client name, matter type, scope description, and contact email from the intake step
   - Use add_note to document the research summary, compliance review outcome, and the approving partner's comments
3. If REJECTED:
   - Do NOT create any record
   - Summarize the rejection reason

## Output Format
If approved:
RECORD CREATED: [onboarding ID]
STATUS: Pending
NOTES ADDED: [confirmation of what was documented]

If rejected:
RECORD NOT CREATED
REASON: [rejection reason from partner]
```

5. Add **MCP tools** — connect to the onboarding tracker at your App Service URL with `/mcp` appended (the same MCP server from Unit 5, e.g., `https://app-xxxx.azurewebsites.net/mcp`)
6. Do NOT add Bing or knowledge base — this agent only needs to create records
7. Select the **Node settings** tab in the Agent Builder, select the **Input message as** and select `Local.approval_decision`.
8. Click **Done** to save the agent and return to the workflow canvas

This is the only agent in the workflow with write access to the onboarding tracker. The Intake Agent can't create records. The Research Agent can't create records. The Compliance Reviewer can't create records. Only the Activation Agent — running as the final step, after human approval — can write to the system.

> **💡 Tip:** This is a governance pattern: **least-privilege per step**. Each agent in the workflow has only the tools it needs for its specific task. No single agent has access to everything. If you were connecting to a real practice management system, this pattern ensures that only the final, post-approval step can create billable matters.

---

### Step 7: Connect the Steps and Configure Variables

Now that all five steps are on the canvas, let's wire them together.

1. **Verify the sequence**: Make sure the steps are connected in order:
   - intake-collector → client-researcher → compliance-reviewer → partner-approval → record-creator

2. **Review the complete flow**: Step back and look at the entire canvas. You should see five connected steps forming a linear pipeline. Each step has:
   - A specialized agent (or human gate)
   - Specific tools assigned (not all tools)
   - Clear input/output variables

> **📝 Note:** The variable names and configuration will depend on the specific Foundry portal UI at the time of the workshop. The instructor will guide you through the exact variable setup. The important concept is that **each step's output becomes the next step's input** — creating a chain of context that flows through the entire pipeline.

---

### Step 8: Test the Complete Workflow

Time to run the workflow end-to-end and see the difference from a prompt agent.

1. Click **Run** or **Preview** in the workflow builder
2. Enter the initial message:

```
I need to onboard a new client — Fabrikam Industries. They're a manufacturing
company that needs help with a contract dispute with one of their suppliers. Its a litigation case. No prior relationship with our firm.
The primary contact is James Liu, james.liu@fabrikam.com. Estimated value
is around $200,000.
```

3. **Watch each step execute in sequence:**

   - **Step 1 (Intake):** The intake-collector agent processes the message, asks follow-up questions if needed, and outputs the structured intake details
   - **Step 2 (Research):** The client-researcher agent searches Bing for "Fabrikam Industries" background, recent news, and legal history — then outputs the research brief
   - **Step 3 (Compliance):** The compliance-reviewer checks the intake against the firm handbook, verifies the engagement value meets thresholds, and generates the partner summary
   - **Step 4 (Approval):** The workflow **pauses**. You see the executive summary and are prompted to approve or reject. Enter "Approved" to continue.
   - **Step 5 (Activation):** The record-creator uses the MCP tool to create the onboarding record and adds notes with the research and compliance summaries

4. After the workflow completes, open the **onboarding tracker dashboard** in your browser (your App Service URL from the Azure Portal). You should see the new Fabrikam Industries record — created through a five-step, human-approved workflow.

**Now compare this to the prompt agent approach:** With the onboarding-agent from Unit 5, you'd send the same message and the agent would flexibly handle research, policy checking, and record creation in a single conversation. That works well for ad-hoc tasks. But the workflow gives you **guaranteed step ordering, a formal human approval gate, and a clear audit trail** of what each step produced — exactly what a regulated process requires.

> **📝 Note:** Watch the workflow's execution timeline or step-by-step log in the portal. You can see exactly what each step produced, how long it took, and what data was passed to the next step. This auditability is critical for legal firms — you can demonstrate to compliance that every intake followed the same process.

---

### Step 9: See What Happens When a Step Flags an Issue

Run the workflow again, but this time test what happens when compliance raises a concern.

1. Start a new workflow run with this input:

```
New client onboarding needed: Consolidated Holdings LLC. They need representation
for a regulatory compliance matter involving environmental regulations. Contact
is Sarah Chen, s.chen@consolidated.com. No estimated value provided.
```

2. Watch the steps execute:

   - **Step 1 (Intake):** Collects the details — but notice that the estimated value is missing
   - **Step 2 (Research):** Researches Consolidated Holdings — may find regulatory or environmental news
   - **Step 3 (Compliance):** Should flag issues: missing estimated value (required by firm policy), regulatory matter may require additional compliance review, and no prior relationship verification

3. When the workflow reaches **Step 4 (Approval)**, review the compliance summary. You should see flags about the missing information and regulatory sensitivity. This time, enter **"Rejected — need estimated engagement value before proceeding"**

4. **Step 5 (Activation):** The record-creator sees the rejection and does NOT create a record. It outputs the rejection reason.

This is exactly how it should work. The workflow caught the issue at Step 3, surfaced it to the partner at Step 4, and the partner sent it back. No record was created. No incomplete matter entered the system. **The process protected the firm from an incomplete intake — automatically.**

---

## Summary

🎉 **Congratulations — you've built your first workflow agent!**  You moved from a single prompt agent that makes its own decisions to a **multi-step, human-governed pipeline** where you control every aspect of the flow.

| Unit | What You Added | Capability |
|------|---------------|------------|
| **Unit 1** | Declarative agent + instructions | Agent has a persona and can chat |
| **Unit 2** | Grounding with Bing | Agent searches the web for current information |
| **Unit 3** | File-based knowledge grounding | Agent answers from uploaded documents with citations |
| **Unit 4** | Structured instructions + conversational flow | Agent has scope boundaries, consistent personality, conversational patterns, and a structured intake workflow |
| **Unit 5** | MCP tools + onboarding tracker | Agent creates records, updates status, and takes real actions |
| **Unit 6** | Workflow agents | Multi-step pipeline with human approval and controlled flow |

### Key Takeaway

The difference between a prompt agent and a workflow agent isn't intelligence — it's **purpose**. A prompt agent is like a versatile associate who can handle any question you throw at them — flexible, adaptive, and great for open-ended work. A workflow agent is like a case management checklist where each step is handled by a specialist, the sequence is defined, and nothing moves forward without the right sign-off. Both are valuable. For legal firms, where many processes require defined steps and formal approvals, workflows are how you bring that structure to AI-powered automation.

### What's Next

In **[Unit 7: Safety & Governance](./unit-7-safety-governance.md)**, you'll add the final layer of production readiness — content safety filters, PII detection to protect privileged information, and governance controls that ensure your agents and workflows operate within the boundaries your firm requires.

---

## Key Concepts

- **Workflow Agent** — A multi-step pipeline where you define the exact sequence of agents, logic blocks, and human gates. You control the order of operations and which tools each step can access.

- **Sequential Workflow** — Steps execute one after another in a fixed order. Each step's output becomes the next step's input — the right pattern for processes with mandatory steps.

- **Human-in-the-Loop** — A workflow step that pauses execution and waits for a human to make a decision. No AI reasoning happens — it's a genuine decision point.

- **Least-Privilege Per Step** — Each agent in a workflow gets only the tools it needs. The Intake Agent has no tools. The Research Agent has Bing. The Activation Agent has MCP. No single agent has access to everything.

- **Variable Passing** — Data flows between workflow steps via variables (e.g., `intake_details`, `research_brief`). This creates a chain of context without any single agent holding the entire conversation history.

- **Auditability** — Each workflow step logs its input, output, and duration — creating a compliance trail showing every intake followed the defined process.

> **💡 Tip:** Think about the processes at your firm that follow a fixed sequence: client intake, conflict checks, engagement approvals, document reviews, matter closings. Each of these is a candidate for a workflow agent. Start by mapping the steps on paper (or a whiteboard), identifying which steps need AI intelligence vs. human judgment, and then build the workflow in Foundry. The visual builder makes it straightforward to translate a process diagram into a working pipeline.

### When to Go Pro-Code for Workflows

Everything in this unit was built through the Foundry portal — no code required. The visual workflow builder handles sequential pipelines, human approval gates, and variable passing between steps. But as your firm's workflows grow more complex, you may hit scenarios where the portal's visual builder isn't enough. That's when you'd reach for an orchestration framework — such as the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework), SDKs available for Python and .NET, or other multi-agent orchestration framework.

| Scenario | Why pro-code? |
|----------|--------------|
| **Parallel execution** | Run due diligence and conflicts check simultaneously (fan-out), then merge results (fan-in). The portal supports sequential steps; code-based orchestration supports concurrent patterns natively. |
| **Dynamic agent routing** | A triage agent that inspects the matter type and routes to the right specialist agent (litigation, corporate, regulatory) — with the AI deciding the routing at runtime. |
| **Custom error handling** | Retry a failed Bing search, fall back to a different research source, or escalate to a human if an agent fails. Code gives you lifecycle hooks and recovery patterns for production resilience. |
| **Agent-to-Agent communication** | Agents that talk to each other directly — enabling cross-system or even cross-firm agent collaboration using protocols like A2A. |
| **Integration with CI/CD** | Version your agent definitions and orchestration logic in Git, deploy through a pipeline, and manage with the same DevOps practices your engineering team already uses. |