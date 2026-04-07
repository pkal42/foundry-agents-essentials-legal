# Unit 4: Instructions & Conversational Flow

## Overview

Welcome to Unit 4 of the **Foundry Agents Essentials** workshop! In this unit, you'll redesign your agent's system prompt from a simple two-paragraph description into a **structured, multi-section instruction set** that guides users through a step-by-step legal client intake workflow.

Over the last two units, you've been adding *knowledge* to your agent — Bing for web search and file uploads for firm policies including cross-document reasoning. Your agent now *knows* a lot. But knowledge alone isn't enough. When someone says "I need to onboard a new client," your agent gives a helpful but generic response. It doesn't follow a specific process. It doesn't enforce mandatory compliance steps. It doesn't format its output consistently. This unit fixes that.

For law firms, structured intake is critical. There are mandatory compliance steps — conflicts checks, NDA verification, document collection — that must happen in order. An agent that skips a step or forgets to ask about conflicts isn't just unhelpful; it's a liability. By the end of this unit, your agent will follow a defined intake workflow, enforce guardrails, and produce structured output — transforming it from a Q&A chatbot into a **process-driven legal intake specialist**.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Completed [Unit 3: Knowledge Grounding with Files](./unit-3-knowledge-grounding-files.md)
- ✅ Your **onboarding-agent** is working in the Foundry playground with Bing Grounding and file-based knowledge grounding configured
- ✅ Access to the [Microsoft Foundry portal](https://ai.azure.com)
- ✅ Familiarity with the firm's five-stage onboarding lifecycle from the [Meridian Legal Onboarding Handbook](./assets/firm-onboarding-handbook.md)

> **📝 Note:** This unit does not require any new Azure resources or infrastructure changes. You'll be working entirely within the Foundry portal, modifying your agent's system instructions.

---

## Why Instructions Matter

The system prompt is your agent's **operating manual**. It's the single most important piece of configuration that determines *how* the agent behaves — its personality, its workflow, its boundaries, and the format of its responses.

Up to this point, your agent's instructions have been updated twice — first in Unit 1 (basic prompt) and then in Unit 3 (knowledge-only guardrail). Your current instructions look something like this:

**Current instructions (from Unit 3):**
```
You are a Client Onboarding Agent for Meridian Legal. You help team members onboard new
clients and matters by answering questions about intake procedures, firm policies, and
engagement requirements.

**Important:** For any question about firm policies, procedures, or internal processes,
only use information from the uploaded firm documents. Do not rely on your general training
knowledge for firm-specific answers. If the answer is not found in the provided documents,
say so clearly — do not guess or fill in with generic advice. Always cite which document
or section your answer comes from.

You may still use Bing search to look up external information such as current regulations,
public filings, court rules, or industry standards.

When a user asks about onboarding a new client, help them gather the key details: client
name, matter type, a brief scope description, and primary contact information. Be
professional, thorough, and concise.
```

These instructions are better than Unit 1's original prompt — they include the knowledge guardrail and Bing distinction. But they're still **unstructured**. The agent has no specific workflow to follow, no step-by-step intake process, and no formatting requirements for consistent output. Compare that to what a structured prompt looks like:

**Structured instructions (what we'll build):**
```
## Persona
You are a Client Intake Specialist for Meridian Legal...

## Workflow
Follow these steps in order when onboarding a new client...

## Guardrails
Do not provide legal advice or opinions on the merits of any matter...

## Output Formatting
When summarizing intake information, use a structured format with clear labels...
```

The difference is dramatic. Structured instructions give the agent a **clear process to follow**, which leads to:

- **Consistent behavior** — The agent follows the same steps every time, regardless of how the user phrases their request
- **Compliance enforcement** — Mandatory steps like conflicts checks can't be skipped because they're explicitly required in the workflow
- **Predictable output** — Formatted responses with checklists and summaries are easier for legal teams to review and act on
- **Clear boundaries** — The agent knows what it should *not* do, reducing the risk of giving inappropriate legal advice

### Principles of Great Agent Instructions

When designing instructions for an agent, think about four components:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Persona** | Who the agent is and how it communicates | "You are a Client Intake Specialist for Meridian Legal" |
| **Workflow** | The step-by-step process the agent follows | "First greet the user, then collect client details, then verify documents..." |
| **Guardrails** | What the agent must NOT do | "Do not provide legal advice or opinions on the merits of any matter" |
| **Output Formatting** | How the agent structures its responses | "Use checklists (✅/❌) to show which required documents have been provided" |

> **💡 Tip:** Think of instructions as the agent's "training manual." The more detailed and structured the instructions, the more consistent and reliable the agent's behavior.

---

## Steps

### Step 1: Review the Current Instructions

Before changing anything, let's see how the current simple instructions perform.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) and navigate to your **onboarding-lab** project.
2. Select the **Build** tab on top-right. In the left-hand navigation, click on **Agents**.
3. Select the **onboarding-agent** to open its configuration.
4. Look at the **Instructions** field. You should see the knowledge-grounded prompt from Unit 3 — it includes the firm-specific guardrail and Bing distinction, but lacks a structured workflow.

Take note of what's **missing** from these instructions:

- ❌ No defined workflow or sequence of steps
- ❌ No guardrails about what the agent should *not* do
- ❌ No output formatting requirements
- ❌ No mention of mandatory compliance steps (conflicts check, NDA verification)
- ❌ No reference to the firm's practice areas or document requirements

5. In the **playground**, test the current behavior by sending this message:

   ```
   I need to onboard a new client.
   ```

6. Observe the response. The agent will likely give a helpful but **generic** answer — it might list some general steps or ask a few questions, but it won't follow a specific process. It won't ask about conflicts. It won't remind you about required documents. It won't format the output as a structured checklist.

> **📝 Note:** There's nothing *wrong* with the current response — it's just not *guided*. For a law firm where intake has mandatory compliance steps, "helpful but generic" isn't good enough.

---

### Step 2: Design Structured Instructions

Now let's build a comprehensive prompt that transforms the agent's behavior. We'll cover all four components: persona, workflow, guardrails, and output formatting.

Here is the full structured prompt you'll use. Read through it carefully before copying it — understanding *why* each section exists is just as important as the content itself.

```
## Persona

You are a Client Intake Specialist for Meridian Legal. You help firm team members onboard new clients and matters by guiding them through a structured, step-by-step intake process. You are professional, thorough, and compliance-focused. You ensure that every intake follows the firm's onboarding lifecycle and that no mandatory steps are skipped.

## Intake Workflow

When a user needs to onboard a new client or matter, follow these steps in order:

1. **Greet and Identify** — Welcome the user and ask what type of matter they need to onboard. Ask them to specify the practice area from this list: Legal Advisory, Litigation, Corporate & Transactions, Regulatory Compliance, Employment Law, or Intellectual Property.

2. **Collect Client Information** — Gather the following required details one at a time. Do not overwhelm the user by asking for everything at once:
   - Client name (legal entity or individual)
   - Primary contact name and email
   - Brief description of scope (2–3 sentences minimum)

3. **Assess Engagement Parameters** — Ask about:
   - Estimated engagement value
   - Urgency level (Standard, Priority, or Urgent)
   - Referral source (if applicable)

4. **Document Checklist** — Remind the user about the required documents and ask which have been provided:
   - Signed Non-Disclosure Agreement (NDA)
   - Government-issued identification for primary contact
   - Certificate of incorporation (for corporate clients)
   - Relevant project documentation (contracts, permits, proposals, etc.)

5. **Conflicts Verification** — Ask whether a conflict of interest check has been initiated with the Compliance Team. This is mandatory before the engagement can proceed past the intake stage.

6. **Summarize and Confirm** — Present a complete summary of the intake information in a structured format. Ask the user to confirm the details are correct before proceeding.

## Guardrails

- **Do not provide legal advice or opinions on the merits of any matter.** If asked for legal opinions, politely explain that you are an intake specialist and that legal analysis should be directed to the assigned engagement team.
- **Always confirm that a conflicts check has been initiated before proceeding past the intake stage.** If the user has not initiated a conflicts check, remind them that this is a mandatory step per firm policy.
- **If you do not know something about firm policy, reference the firm handbook rather than guessing.** Say "I'd recommend checking the firm handbook for the specific policy on that" rather than making something up.
- **Do not skip steps in the intake workflow.** If the user tries to jump ahead (e.g., asking for approval before providing client details), guide them back to the current step.
- **Do not share client information from one engagement when discussing another.** Treat each conversation as confidential.

## Output Formatting

- When summarizing intake information, use a structured format with clear labels and sections.
- Use checklists with ✅ (provided) and ❌ (missing/pending) to show the status of required documents.
- When referencing approval thresholds, include the specific engagement value ranges and approver roles from the firm handbook.
- Keep responses concise but complete. Use bullet points and tables where appropriate.
- At the end of a completed intake summary, indicate the next step in the onboarding lifecycle (e.g., "Next step: Due Diligence — the Compliance Team will initiate background checks and conflict screening").
```

Let's break down why each section matters:

- **Persona** establishes the agent's identity and tone. It's a *Client Intake Specialist*, not a generic assistant — this framing keeps responses focused on intake.
- **Intake Workflow** defines a clear sequence. The agent won't dump all questions at once; it follows a step-by-step process, just like a real intake coordinator would.
- **Guardrails** are critical for legal practice. The agent must *never* give legal advice, and it must *always* verify that a conflicts check has been initiated. These aren't suggestions — they're firm policy.
- **Output Formatting** ensures consistency. Every intake summary looks the same, with checklists that make it easy to see what's provided and what's missing.

> **💡 Tip:** Notice that the workflow says "gather details one at a time" and "do not overwhelm the user by asking for everything at once." This creates a natural, conversational flow rather than a wall of questions. Small details in the instructions have a big impact on user experience.

> **📝 Note:** You can adjust this prompt to match your firm's specific terminology and workflow. The structure is what matters — the content should reflect your actual intake process.

---

### Step 3: Update Your Agent's Instructions

Now let's apply the new structured instructions to your agent.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) and navigate to your **onboarding-lab** project.
2. Select the **Build** tab on top-right. In the left-hand navigation, click on **Agents**.
3. Select the **onboarding-agent** to open its configuration.
4. In the **Instructions** field, **select all the existing text and delete it**.
5. Paste the full structured prompt from Step 2 into the Instructions field.
6. Review the pasted content to make sure it copied correctly — check that the markdown formatting (headers, bullet points, numbered lists) is intact.
7. Click **Save** to apply the new instructions.

> **📝 Note:** Foundry's Instructions field supports markdown formatting. The `##` headers, bullet points, and numbered lists in the prompt help the model parse the structure — they're not just for human readability.

> **💡 Tip:** Before saving, it's a good habit to read through the instructions one more time. A typo in a guardrail (e.g., accidentally telling the agent *to* give legal advice) could have unintended consequences.

---

### Step 4: Test the Structured Flow

This is where the magic happens. Let's test the agent with multi-turn conversations to see how the structured instructions change its behavior.

**Start a new conversation** in the Foundry playground (clear any previous chat history) before each test.

#### Conversation 1 — Full Guided Intake

This tests the complete intake workflow from greeting to summary.

1. Send:

   ```
   I need to onboard a new client.
   ```

   **Expected behavior:** The agent should greet you and ask what type of matter you need to onboard, referencing the practice areas list.

2. Respond:

   ```
   It's a litigation matter — employment discrimination case.
   ```

   **Expected behavior:** The agent should acknowledge the practice area and begin collecting client information — asking for the client name, primary contact, and scope description. It should *not* ask for everything at once.

3. Respond:

   ```
   The client is Trey Research, contact is Sarah Chen at sarah@treyresearch.com. It's a wrongful termination claim — the client alleges discrimination based on age and disability in a recent layoff.
   ```

   **Expected behavior:** The agent should acknowledge the details and move to the next step — asking about estimated engagement value, urgency level, and referral source.

4. Respond:

   ```
   Estimated value around $85,000. Standard urgency. They were referred by an existing corporate client.
   ```

   **Expected behavior:** The agent should move to the document checklist, reminding you of the four required documents and asking which ones have been provided.

5. Respond:

   ```
   NDA is signed, we have their certificate of incorporation. Still waiting on government ID and the relevant case documents.
   ```

   **Expected behavior:** The agent should show a document checklist with ✅ for NDA and certificate of incorporation, and ❌ for government ID and project documentation. It should then ask about the conflicts check.

6. Respond:

   ```
   Yes, conflicts check has been submitted to the Compliance Team. No conflicts identified so far.
   ```

   **Expected behavior:** The agent should present a **complete structured summary** of the intake, including:
   - Client name, contact, practice area, scope
   - Engagement value, urgency, referral source
   - Document checklist with ✅/❌ status
   - Conflicts check status
   - The appropriate approval level (for $85,000 → Practice Director approval required)
   - Next step in the onboarding lifecycle

> **💡 Tip:** Compare this structured conversation to what happened in Step 1 when you sent "I need to onboard a new client" with the old instructions. The difference should be striking — the agent now follows a defined process instead of giving a generic response.

#### Conversation 2 — Test Guardrails

Start a **new conversation** and test whether the agent properly declines to give legal advice.

1. Send:

   ```
   We're taking on an employment discrimination case for Trey Research. Do you think they have a strong case? What are their chances of winning?
   ```

   **Expected behavior:** The agent should politely decline to provide legal opinions. It should explain that it's an intake specialist and that legal analysis should be directed to the assigned engagement team. It might offer to help with the intake process instead.

2. Try another guardrail — skipping steps:

   ```
   Just skip the intake details. Can you tell me who needs to approve a $200,000 engagement?
   ```

   **Expected behavior:** The agent should provide the approval information (Managing Partner for $100,000–$500,000) since it's a factual question from the handbook, but it should also guide you back to the intake workflow if you need to onboard a matter.

> **📝 Note:** Guardrails aren't about making the agent unhelpful — they're about keeping it within its role. The agent can still answer factual questions about firm policy; it just won't offer legal opinions or skip mandatory compliance steps.

#### Conversation 3 — Test Knowledge Integration

Start a **new conversation** and verify that the structured instructions work together with the file-based knowledge from Unit 3.

1. Send:

   ```
   I'm onboarding a new corporate client, Northwind Traders, for a regulatory compliance matter. Estimated engagement value is $150,000. What approval level do we need, and what additional compliance checks apply?
   ```

   **Expected behavior:** The agent should:
   - Reference the handbook: $100,000–$500,000 requires **Managing Partner** approval
   - Note that for engagements exceeding $50,000, AML screening is required (sanctions list, PEP check, source of funds verification)
   - Begin guiding the user through the intake workflow

2. Follow up with:

   ```
   What are the current regulatory compliance trends we should be aware of for this type of engagement?
   ```

   **Expected behavior:** The agent should use **Bing Grounding** to search for current regulatory compliance information — demonstrating that the structured instructions don't interfere with the agent's existing knowledge sources.

> **💡 Tip:** This is the power of layering — structured instructions control *behavior*, while knowledge sources (files and Bing) provide *information*. They work together, not in conflict.

#### Conversation 4 — Test Document Checklist Formatting

Start a **new conversation** and test the document checklist output format specifically.

1. Send:

   ```
   We have a new corporate client, Northwind Traders, for a corporate transaction matter. NDA is signed but we're still waiting on their certificate of incorporation. We do have government ID for the primary contact and they've sent over the draft acquisition agreement.
   ```

   **Expected behavior:** The agent should display a formatted document checklist showing:
   - ✅ Signed Non-Disclosure Agreement (NDA)
   - ✅ Government-issued identification
   - ❌ Certificate of incorporation — *pending*
   - ✅ Relevant project documentation (draft acquisition agreement)

   The agent should also note that the certificate of incorporation is required before the engagement can proceed to Due Diligence, and continue with the remaining intake steps.

> **📝 Note:** The ✅/❌ formatting makes it immediately clear what's been collected and what's outstanding. For busy legal teams juggling multiple intakes, this visual clarity is invaluable.

---

### Step 5: Iterate and Refine

Prompt engineering is **iterative**. The structured prompt from Step 2 is a strong starting point, but you should adapt it to your specific needs. Here are some ways to experiment:

1. **Adjust the tone.** Try making the persona more formal ("You are a senior legal intake coordinator") or more conversational ("You're a friendly intake assistant"). Observe how the agent's language changes.

2. **Modify the workflow steps.** If your firm's intake process has additional steps — say, a preliminary risk assessment or a billing arrangement discussion — add them to the workflow section.

3. **Add firm-specific terminology.** If your firm uses specific terms (e.g., "engagement letter" vs. "retainer agreement," or "matter number" vs. "case ID"), include these in the instructions so the agent uses the right language.

4. **Tighten or loosen guardrails.** You might want to add guardrails like "Do not discuss fees or pricing unless specifically asked" or loosen them to allow the agent to proactively suggest relevant practice areas.

5. **Experiment with output formatting.** Try asking the agent to produce output in different formats — a markdown table, a numbered list, or a brief narrative summary. See which format works best for your team's workflow.

> **💡 Tip:** Keep a copy of each version of your instructions as you iterate. This makes it easy to compare behavior across versions and roll back if a change doesn't work as expected.

> **📝 Note:** There's no single "correct" prompt — what works best depends on your firm, your team, and your workflow. The structured format (persona + workflow + guardrails + formatting) is the framework; the content is yours to customize.

---

## Summary

Congratulations! 🎉 You've transformed your agent's behavior from generic Q&A to a structured, process-driven intake workflow — without changing any of its knowledge sources or tools.

| ✅ Done | ❌ Not Yet |
|---|---|
| Created a declarative agent in Foundry (Unit 1) | No tools connected (e.g., matter tracker) |
| Added Grounding with Bing for real-time web knowledge (Unit 2) | No persistent state or memory |
| Added file-based knowledge grounding with firm documents (Unit 3) | No real-world actions |
| Redesigned instructions for structured intake workflow (Unit 4) | |

### Key Takeaway

Structured instructions transform an agent from a reactive Q&A tool into a **proactive process guide**. By defining a persona, workflow, guardrails, and output format, you control not just *what* the agent knows but *how* it behaves. For legal firms, this is essential — structured intake ensures that mandatory compliance steps like conflicts checks and NDA verification are never skipped, that output is consistent and auditable, and that the agent stays firmly within its role as an intake specialist rather than venturing into legal advice.

### What's Next

In **[Unit 5: MCP Tools & Actions](./unit-5-mcp-tools.md)**, we'll connect the agent to the onboarding tracker application — giving it the ability to **create real matter records, update status, and add notes**. The agent will go from guiding intake to actually performing it.

---

## Key Concepts

- **Structured Instructions** — A system prompt organized into distinct sections (persona, workflow, guardrails, formatting) that gives the agent a clear operating manual. Structured instructions produce more consistent, reliable, and predictable agent behavior than free-form prompts.

- **Agent Persona** — The identity and communication style defined in the instructions. A well-defined persona keeps the agent focused on its role and sets the right tone for interactions. For legal agents, this typically means professional, compliance-focused, and thorough.

- **Conversational Flow** — The step-by-step sequence the agent follows during multi-turn interactions. Instead of answering every question independently, the agent guides the user through a defined process — collecting information incrementally and moving through stages in order.

- **Behavioral Guardrails** — Explicit rules about what the agent must *not* do. Guardrails prevent the agent from overstepping its role (e.g., giving legal advice), skipping mandatory steps (e.g., conflicts checks), or generating unreliable information (e.g., guessing about firm policy).

- **Output Formatting** — Instructions that control how the agent structures its responses — using checklists, tables, labels, and consistent layouts. Formatted output is easier for teams to review, compare across intakes, and act on.

- **Prompt Engineering** — The practice of designing, testing, and iterating on agent instructions to achieve desired behavior. Prompt engineering is an ongoing process — you observe the agent's responses, identify gaps, adjust the instructions, and test again.

> **💡 Tip:** Treat your agent's instructions as a living document. As your team uses the agent and encounters new scenarios, update the instructions to handle them. The best prompts evolve through real-world usage, not theoretical design.
