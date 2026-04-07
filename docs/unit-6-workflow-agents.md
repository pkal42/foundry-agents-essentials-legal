# Unit 6: Workflow Agents

## Overview

Welcome to Unit 6 of the **Foundry Agents Essentials** workshop! Up to this point, every agent you've built has been a **prompt agent** — a single agent that receives a user message, reasons about what to do, and responds. Prompt agents are powerful, but they have a fundamental limitation: **the AI decides the flow**. When your agent has access to Bing search, a knowledge base, MCP tools, and structured instructions, it *should* research the client, check firm policies, run a conflicts screening, and then create the onboarding record — in that order. But it *might not*. It might skip the research. It might create the record before checking conflicts. It might do everything right for one user and something different for the next.

For legal firms, that's a problem. Client intake isn't a conversation — it's a **process**. There are mandatory steps that must happen in a specific order, every time, for every client. A conflicts check must complete before an engagement letter is drafted. A partner must approve before the matter becomes active. These aren't suggestions — they're requirements. You can't leave the sequence up to an AI's judgment.

**Workflow agents solve this.** Instead of giving one agent all the tools and hoping it follows the right sequence, you build a **workflow** — a visual, step-by-step pipeline where **you define the exact order of operations**. Each step runs a specialized agent (or a logic block, or a human approval gate), and the next step doesn't start until the previous one completes. The AI still powers the intelligence within each step, but **you control the flow between steps**.

This is the most important architectural shift in the workshop: moving from "the AI decides" to "I decide, and the AI executes."

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Infrastructure deployed via `azd up`
- ✅ Access to the [Microsoft Foundry portal](https://ai.azure.com)

> **📝 Note:** This unit introduces the **Workflows** feature in Microsoft Foundry. Workflows are created and managed through the Foundry portal — no code, no YAML, no SDK. You'll use the visual workflow builder to design, connect, and test your multi-step pipeline.

---

## Prompt Agents vs. Workflow Agents

Before we build anything, let's understand *why* workflow agents exist and when you need them.

### The Problem with "Smart" Agents

Over the past six units, you've built a highly capable prompt agent. It can:

- Research a prospective client using Bing (Unit 2)
- Look up firm policies from uploaded documents (Unit 3)
- Guide the user through a structured intake conversation (Unit 4)
- Create onboarding records via MCP tools (Unit 5)

That's impressive.But here's the catch: when a user says "I need to onboard Contoso Ltd as a new client," the agent decides on its own which of those capabilities to use and in what order. Sometimes it researches the client first. Sometimes it jumps straight to collecting intake details. Sometimes it checks firm policy. Sometimes it doesn't. The behavior is **probabilistic** — it varies based on how the user phrases the request, the conversation context, and the model's reasoning.

For a marketing chatbot, that's fine. For legal client intake, it's not.

### What Legal Firms Actually Need

Legal client intake follows a defined process — the five-stage onboarding lifecycle from your [firm handbook](./assets/firm-onboarding-handbook.md):

| Stage | What Happens | Can It Be Skipped? |
|-------|-------------|-------------------|
| **1. Intake** | Collect client details, matter type, scope | ❌ Never |
| **2. Due Diligence** | Research the client, check for conflicts | ❌ Never |
| **3. Scope & Proposal** | Summarize the engagement for partner review | ❌ Never |
| **4. Approval** | Partner reviews and approves | ❌ Never |
| **5. Activation** | Create the matter record in the system | ❌ Never |

Every step must happen. Every step must happen in order. A prompt agent *might* follow this sequence, but it *can't guarantee it*. A workflow agent **does guarantee it** — because you build the sequence yourself.

### The Key Difference

| | Prompt Agent | Workflow Agent |
|---|---|---|
| **Who controls the flow?** | The AI decides which tools to call and in what order | You define the exact sequence of steps |
| **Can steps be skipped?** | Yes — the AI may skip steps based on its reasoning | No — every step runs, in order |
| **Consistency** | Varies per conversation | Same process every time |
| **Human approval** | Not built in — the AI can't pause and wait for a human | Built in — workflow pauses at approval gates |
| **Auditability** | Hard to verify what happened | Each step logs its input and output |
| **Best for** | Open-ended Q&A, research, exploration | Defined processes with mandatory steps |

> **💡 Tip:** Prompt agents and workflow agents aren't competing approaches — they're complementary. In this unit, you'll build a workflow that *uses* prompt agents as steps. The workflow controls the sequence; the prompt agents handle the intelligence within each step. Think of it as: **the workflow is the process; the agents are the workers.**

### What About Multi-Agent Orchestration?

There's a third pattern worth understanding: **agentic orchestration** — where a "manager" agent dynamically decides which specialist agents to call, routes tasks between them, and merges their results. Think of a triage agent that receives a legal inquiry, determines whether it's a litigation matter or a corporate transaction, and delegates to the right specialist agent autonomously.

That pattern is powerful, but it's **not available through the portal**. Dynamic agent-to-agent delegation — where the AI decides the routing — requires pro-code using an orchestration framework such as the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework), SDKs available for Python and .NET, or other multi-agent orchestration framework.

Here's how the three approaches compare:

| Pattern | Who controls the flow? | Built in portal? | When to use |
|---------|----------------------|-------------------|-------------|
| **Prompt Agent** (Units 1–6) | AI decides tool usage within one agent | ✅ Yes | Open-ended Q&A, research, exploration |
| **Workflow Agent** (this unit) | You define the step sequence | ✅ Yes | Mandatory processes with fixed steps |
| **Agentic Orchestration** | AI routes between multiple agents dynamically | ❌ Pro-code | Complex routing, triage, specialist delegation |

For this use case, **workflow agents are the right fit** — legal intake is a defined process with mandatory steps, not a dynamic routing problem. But as your firm's AI maturity grows and you start building agents that need to triage across practice areas or dynamically assemble specialist teams, pro-code orchestration is the natural next step — and everything you've built in the portal carries forward.

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
2. In the left navigation pane, click on **Build**, then select **Agents**, then the **Workflows** tab
3. Click **Create workflow**
4. You'll see workflow template options. Select **Sequential** — this creates a linear, step-by-step workflow where each step runs after the previous one completes. You should now see the Visualizer display of the workflow with three agent cards and a sequential flow created with Start and the Agent cards.
5. Click **Save** and give your workflow a name: `client-intake-workflow`

> **📝 Note:** The sequential template is the right choice for client intake because every step depends on the previous step's output. Foundry also offers **Group Chat** workflows (multiple agents collaborate in a conversation) and **Human-in-the-loop** templates. You'll add a human approval step within the sequential flow.

---

### Step 2: Create the Intake Agent (Step 1 of the Workflow)

The first step in the workflow collects client details. You'll create a specialized prompt agent for this — simpler and more focused than your all-in-one onboarding-agent.

1. On the workflow canvas, click the **+** button to add a new step
2. Select **Agent** as the step type
3. Choose **Create new agent** (or select an existing agent if you prefer)
4. Name it: `intake-collector`
5. Set the model to your deployed model (e.g., `gpt-4.1`)
6. Add the following instructions:

```
## Role
You are a client intake collector for Meridian Legal. Your ONLY job is to gather
the required information for a new client engagement.

## Required Fields
Collect ALL of the following before completing your task:
1. Client name (legal entity or individual)
2. Primary contact name and email
3. Matter type (Litigation, Corporate & Transactions, Regulatory Compliance,
   Employment Law, or Intellectual Property)
4. Brief description of the engagement scope (2-3 sentences)
5. Estimated engagement value (if known)
6. Any known conflicts or prior relationships with this client

## Output Format
When you have all required fields, output a structured summary using this exact format:

CLIENT: [name]
CONTACT: [name, email]
MATTER TYPE: [type]
SCOPE: [description]
ESTIMATED VALUE: [value or "Not provided"]
PRIOR RELATIONSHIP: [yes/no and details]

## Rules
- Do NOT research the client — that happens in a later step.
- Do NOT check firm policies — that happens in a later step.
- Do NOT create any records — that happens in a later step.
- Focus ONLY on collecting complete, accurate intake information.
```

7. Do not add any tools (Bing, knowledge bases, or MCP) to this agent — it only needs to collect information through conversation

Notice how different these instructions are from the all-in-one onboarding-agent. This agent has one job. It can't research, it can't check policies, it can't create records. That's not a limitation — it's the whole point. **Each agent in a workflow does one thing well. The workflow handles the rest.**

> **💡 Tip:** The structured output format (CLIENT, CONTACT, MATTER TYPE, etc.) isn't arbitrary — it makes it easy for the next step in the workflow to parse and use the information. When designing workflow agents, think about how each step's output becomes the next step's input.

---

### Step 3: Create the Research Agent (Step 2 of the Workflow)

The second step researches the client for background, recent news, and potential risks. This is the due diligence step of the onboarding lifecycle.

1. Add another **Agent** step to the workflow canvas (click **+** after the intake-collector step)
2. Create a new agent named: `client-researcher`
3. Set the model to your deployed model
4. Add the following instructions:

```
## Role
You are a client due diligence researcher for Meridian Legal. You receive
intake details from the previous step and research the client.

## Tasks
Using the client information provided:
1. Search for the client company's background — what they do, their size,
   and their industry
2. Find any recent news, press releases, or developments about the client
3. Identify any regulatory actions, lawsuits, or legal issues involving the client
4. Note any reputational risks or red flags

## Output Format
Provide a structured research brief:

COMPANY OVERVIEW: [2-3 sentences]
RECENT DEVELOPMENTS: [bullet points of relevant news]
LEGAL/REGULATORY HISTORY: [any known issues or "No issues found"]
RISK ASSESSMENT: [Low / Medium / High with brief justification]

## Rules
- Base your research on verifiable information from web searches.
- If you cannot find information about the client, state that clearly.
- Do NOT make recommendations about whether to accept the engagement.
- Do NOT create any records or check firm policies.
```

5. Add **Bing Grounding** as a tool for this agent — it needs web search to do its job
6. Do NOT add knowledge bases or MCP tools

**This is the power of workflows**: the Research Agent has Bing grounding, but the Intake Agent doesn't. Each agent gets exactly the tools it needs — nothing more. In a prompt agent approach, one agent has all the tools and the AI decides which to use. In a workflow, **you decide which tools each step can access.**

---

### Step 4: Create the Compliance Review Agent (Step 3 of the Workflow)

The third step checks the intake against firm policies and generates a partner-ready summary. This is where the knowledge from Unit 3 comes in.

1. Add another **Agent** step to the workflow canvas
2. Create a new agent named: `compliance-reviewer`
3. Set the model to your deployed model
4. Add the following instructions:

```
## Role
You are a compliance reviewer for Meridian Legal. You receive client intake
details and a research brief from previous steps. Your job is to review
everything against firm policies and prepare a summary for partner approval.

## Tasks
1. Check the engagement against the firm's onboarding handbook:
   - Does the engagement type match a recognized practice area?
   - Does the estimated value meet the minimum threshold for this practice area?
   - Are all required intake fields complete?
2. Identify any compliance concerns:
   - Prior relationships that need conflicts verification
   - Regulatory sensitivity requiring additional review
   - Engagement value thresholds that require Practice Director vs Managing
     Partner approval
3. Generate a partner-ready executive summary combining the intake details,
   research findings, and compliance assessment

## Output Format
COMPLIANCE STATUS: [Pass / Needs Review / Fail]
ISSUES FOUND: [list any issues, or "None"]
APPROVAL LEVEL REQUIRED: [Practice Director / Managing Partner]
EXECUTIVE SUMMARY: [3-4 sentence brief for the approving partner, covering
who the client is, what they need, the research findings, and any concerns]

## Rules
- Reference specific policies from the firm handbook when flagging issues.
- Be conservative — flag anything that MIGHT need attention.
- Do NOT approve the engagement — that's the partner's decision.
- Do NOT create any records.
```

5. Add your **file-based knowledge** as a tool (the firm documents you uploaded in Unit 3)
6. Do NOT add Bing or MCP tools

Again, this agent has exactly one capability: checking firm policies via the knowledge base. It can't search the web (that already happened in Step 2) and it can't create records (that happens in Step 5). **The workflow ensures each step stays in its lane.**

---

### Step 5: Add a Human Approval Gate (Step 4 of the Workflow)

This is the step that no prompt agent can replicate. The workflow **pauses** and waits for a human to review the summary and make a decision.

1. Add a **Ask a question** step to the workflow canvas (this is a built-in step type, not an agent)
2. Configure the step:
   - **Prompt to reviewer:** Display the compliance-reviewer's output (the executive summary, compliance status, and any flagged issues) and ask the partner to approve or reject
   - **Input options:** The reviewer should be able to provide approval ("Approved" or "Rejected") and optional comments

When the workflow reaches this step, it **stops and waits**. No timer, no timeout, no AI making the decision. A real person — the approving partner — reviews the executive summary from Step 3, sees the research findings from Step 2, and makes a judgment call. Only when they respond does the workflow continue.

**This is why workflows exist for legal firms.** No matter how good the AI is at research, policy checking, and summarization, the approval decision must be made by a human. A prompt agent can't pause mid-conversation and wait for a partner in a different time zone to review the matter. A workflow can.

> **📝 Note:** In a production deployment, you'd configure notifications (email or Teams) to alert the reviewing partner when an approval is waiting. For this workshop, you'll trigger the approval manually during testing.

---

### Step 6: Create the Activation Agent (Step 5 of the Workflow)

The final step creates the onboarding record in the tracker — but only if the partner approved.

1. Add another **Agent** step to the workflow canvas
2. Create a new agent named: `record-creator`
3. Set the model to your deployed model
4. Add the following instructions:

```
## Role
You are the record activation agent for Meridian Legal. You receive approved
client intake details and create the official onboarding record.

## Tasks
1. Review the approval decision from the previous step
2. If APPROVED: Use the create_onboarding tool to create the record using
   the intake details collected in Step 1
3. After creating the record, add a note documenting:
   - The research summary from the due diligence step
   - The compliance review outcome
   - The approving partner's name and any comments
4. If REJECTED: Do not create any record. Summarize the rejection reason.

## Output Format
If approved:
RECORD CREATED: [onboarding ID]
STATUS: Active
NOTES ADDED: [confirmation]

If rejected:
RECORD NOT CREATED
REASON: [rejection reason from partner]
```

5. Add **MCP tools** — connect to the onboarding tracker at your `AZURE_WEBAPP_URL/mcp` endpoint (the same MCP server from Unit 5)
6. Do NOT add Bing or knowledge base — this agent only needs to create records

This is the only agent in the workflow with write access to the onboarding tracker. The Intake Agent can't create records. The Research Agent can't create records. The Compliance Reviewer can't create records. Only the Activation Agent — running as the final step, after human approval — can write to the system.

> **💡 Tip:** This is a governance pattern: **least-privilege per step**. Each agent in the workflow has only the tools it needs for its specific task. No single agent has access to everything. If you were connecting to a real practice management system, this pattern ensures that only the final, post-approval step can create billable matters.

---

### Step 7: Connect the Steps and Configure Variables

Now that all five steps are on the canvas, let's wire them together.

1. **Verify the sequence**: Make sure the steps are connected in order:
   - intake-collector → client-researcher → compliance-reviewer → partner-approval → record-creator

2. **Configure variables**: Workflows use variables to pass data between steps. The key variables are:
   - `intake_details` — The structured output from Step 1 (client name, matter type, scope, etc.)
   - `research_brief` — The due diligence findings from Step 2
   - `compliance_summary` — The review outcome and executive summary from Step 3
   - `approval_decision` — The partner's approve/reject decision from Step 4

3. **Set the trigger**: Configure the workflow to start with a **manual trigger** (for testing). The trigger input should accept the initial user message — such as "I need to onboard a new client"

4. **Review the complete flow**: Step back and look at the entire canvas. You should see five connected steps forming a linear pipeline. Each step has:
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

4. After the workflow completes, open the **onboarding tracker dashboard** in your browser (`AZURE_WEBAPP_URL`). You should see the new Fabrikam Industries record — created through a five-step, human-approved workflow.

**Now compare this to what would happen with a prompt agent:** You'd send the same message to your onboarding-agent from Unit 5, and it *might* research the client, *might* check policies, and *might* create the record — but you can't guarantee the sequence, you can't inject a human approval step, and you can't audit which steps actually ran. The workflow gives you all of that.

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

🎉 **Congratulations — you've built your first workflow agent!** This is the most significant architectural upgrade in the workshop. You moved from a single prompt agent that makes its own decisions to a **multi-step, human-governed pipeline** where you control every aspect of the flow.

| Unit | What You Added | Capability |
|------|---------------|------------|
| **Unit 1** | Declarative agent + instructions | Agent has a persona and can chat |
| **Unit 2** | Grounding with Bing | Agent searches the web for current information |
| **Unit 3** | File-based knowledge grounding | Agent answers from uploaded documents with citations |
| **Unit 4** | Structured instructions + conversational flow | Agent guides users through a step-by-step intake process |
| **Unit 5** | MCP tools + onboarding tracker | Agent creates records, updates status, and takes real actions |
| **Unit 6** | Workflow agents | Multi-step pipeline with human approval and controlled flow |

### Key Takeaway

The difference between a prompt agent and a workflow agent isn't intelligence — it's **control**. A prompt agent is like giving a smart associate all your files, tools, and instructions and saying "handle this." They'll probably do a great job, but you can't guarantee they'll follow every step, and you can't pause them mid-process for partner approval. A workflow agent is like creating a case management checklist where each step is handled by a specialist, the sequence is locked in, and nothing moves forward without the right sign-off. For legal firms, where process compliance isn't optional, workflows are how you move from AI demos to production systems.

### What's Next

In **[Unit 7: Safety & Governance](./unit-7-safety-governance.md)**, you'll add the final layer of production readiness — content safety filters, PII detection to protect privileged information, and governance controls that ensure your agents and workflows operate within the boundaries your firm requires.

---

## Key Concepts

- **Workflow Agent** — A multi-step pipeline that executes a defined sequence of agents, logic blocks, and human gates. Unlike prompt agents where the AI controls the flow, workflow agents give **you** full control over the order of operations, which tools each step can access, and where human decisions are required.

- **Sequential Workflow** — A workflow pattern where steps execute one after another in a fixed order. Each step's output becomes the next step's input. This is the right pattern for processes with mandatory steps that can't be skipped or reordered — like legal client intake.

- **Human-in-the-Loop** — A workflow step that pauses execution and waits for a human to provide input, make a decision, or approve an action. No AI reasoning happens during this step — it's a genuine decision point where a real person (like a reviewing partner) has full control.

- **Least-Privilege Per Step** — A governance pattern where each agent in a workflow receives only the tools it needs for its specific task. The Intake Agent has no tools (conversation only). The Research Agent has Bing (search only). The Activation Agent has MCP (write access). No single agent has access to everything, reducing risk and enforcing separation of concerns.

- **Prompt Agent vs. Workflow Agent** — Prompt agents are best for open-ended tasks where the AI's flexibility is an advantage (research, Q&A, exploration). Workflow agents are best for defined processes where consistency, auditability, and mandatory steps are requirements. Most production systems use both — workflows orchestrate the process, prompt agents handle the intelligence within each step.

- **Variable Passing** — The mechanism by which data flows between workflow steps. Each step produces output variables (e.g., `intake_details`, `research_brief`) that subsequent steps consume as input. This creates a chain of context through the pipeline without any single agent needing to hold the entire conversation history.

- **Auditability** — The ability to review exactly what happened at each step of a workflow: what input it received, what the agent produced, how long it took, and what was passed forward. For legal firms, this creates a compliance trail showing that every intake followed the defined process — a requirement for many regulatory frameworks and client engagement standards.

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

The portal gets you from zero to working workflow — fast. An orchestration framework gets you to production-grade, enterprise-scale systems. For most legal intake scenarios, the portal is all you need. When you're ready to scale, the pro-code path is there.

> **📝 Note:** Going pro-code doesn't mean starting over. Agents you created in the portal can be called from code through Foundry's Agent Service. The investment you make in building and tuning your prompt agents carries forward — you're just changing how they're coordinated.
