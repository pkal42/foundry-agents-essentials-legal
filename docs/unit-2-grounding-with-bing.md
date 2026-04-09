# Unit 2: Grounding with Bing

## Overview

Welcome to Unit 2 of the **Foundry Agents Essentials** workshop! In this unit, you'll supercharge the agent you built in Unit 1 by adding **Grounding with Bing** — giving your agent the ability to search the web for real-time information.

Right now, your onboarding-agent can only respond using the knowledge baked into its underlying language model. That means it can't look up a prospective client's company, check current legal regulations, or find the latest compliance requirements. By adding Bing as a tool, your agent will pull in current, relevant information from the web — and cite its sources.

The best part? You won't write a single line of code. This is the power of declarative agents in Foundry: extending capabilities is a matter of **configuration, not code**.

By the end of this unit, your agent will be able to answer questions about the real world with up-to-date, grounded responses — turning it from a generic chatbot into a research-capable legal assistant.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Completed [Unit 1: Creating a Declarative Agent](./unit-1-declarative-agent.md)
- ✅ Your **onboarding-agent** agent is working in the Foundry playground
- ✅ Infrastructure deployed via `azd up` (this provisions the Bing Grounding resource automatically)
- ✅ Access to the [Azure Portal](https://portal.azure.com) and the [Microsoft Foundry portal](https://ai.azure.com)

> **📝 Note:** The `azd up` deployment from the main README provisions a Grounding with Bing resource in your Azure resource group. If you skipped that step or the resource wasn't created, go back to the [main README](../README.md) and redeploy before continuing.

---

## What is Grounding with Bing?

When you chat with a language model, it generates responses based on patterns learned during training. But that training data has a cutoff date — the model doesn't *know* what happened yesterday, and it can't look things up on the internet. This is where **grounding** comes in.

**Grounding** means connecting a language model to external, authoritative data sources so its responses are based on real, up-to-date information rather than just its training data. Without grounding, a model might:

- Guess at current regulations and get them wrong
- Provide outdated legal or compliance requirements confidently
- "Hallucinate" plausible-sounding but incorrect regulatory information

**Grounding with Bing** is an Azure service that gives your agent the ability to search the web via Bing and incorporate the results into its responses. When your agent receives a question that requires current information, it will:

1. **Search** the web using Bing to find relevant, up-to-date content
2. **Synthesize** the search results into a natural, conversational response
3. **Cite** the sources so the user knows where the information came from

> **💡 Tip:** Think of Grounding with Bing as giving your agent a web browser. Instead of guessing, it can look things up — just like you would when researching a new client or checking the latest regulations and case law.

---

## Steps

### Step 1: Locate Your Bing Grounding Resource

Before configuring the agent, let's verify that the Bing Grounding resource exists in your Azure environment.

1. Open the [Azure Portal](https://portal.azure.com) and sign in with your Azure credentials.
2. Navigate to your **resource group** — this is the one created during the `azd up` deployment.
3. In the resource list, look for a resource with the type **Bing Resource**. It should have been provisioned automatically by the infrastructure templates.
4. Click on the resource to view its details. Take note of:
   - The **resource name**
   - The **location/region** (should be "global")
   - The **pricing tier** (Standard)

> **📝 Note:** You don't need to copy any keys or connection strings — Foundry will handle the connection for you. This step is just to confirm the resource exists and is healthy.

> **💡 Tip:** If you don't see the Bing Grounding resource in your resource group, double-check that `azd up` completed successfully. You can re-run it from the repository root if needed.

---

### Step 2: Add Bing Grounding to Your Agent

Now let's connect the Bing Grounding resource to your onboarding-agent.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) and navigate to your project.
2. Select the **Build** tab on top-right. In the left-hand navigation, click on **Agents**.
3. Select the **onboarding-agent** agent you created in Unit 1 to open its configuration.
4. Scroll down to the **Tools** section of the agent configuration. Remove the default **Web search (preview)** tool if one is present.
5. Click **Add** and browse all the available tools.
6. From the list of available tool types, select **Grounding with Bing Search**.
7. Foundry will prompt you to connect the resource:
   - Select the **Bing Grounding resource** from your Azure subscription.
   - Confirm the connection.
8. Once added, you should see **Grounding with Bing Search** listed under the Tools section.
9. **Save** your agent configuration.

> **💡 Tip:** You don't need to change your agent's instructions to use Bing Grounding. The agent will automatically decide when to search the web based on the user's question. If the question can be answered from the model's training data alone, it may not trigger a web search — and that's fine.

> **📝 Note:** It may take a moment for the tool to become active after saving. If your first test doesn't show web results, wait a few seconds and try again.

---

### Step 3: Test the Enhanced Agent

Time to see the difference Bing Grounding makes! Let's test with questions that require current information — the kind of research you'd do when onboarding a new client at a law firm.

1. In the Foundry portal, open the **playground** for your onboarding-agent.
2. Start by researching a prospective client:

   ```
   I'm onboarding a new client — MCO. What can you tell me about this company? Any recent updates that I need to be aware of?
   ```

3. Observe the response. You should notice:
   - ✅ The agent provides **current, relevant information** about the company
   - ✅ The response includes **citations or source references** indicating where the information came from
   - ✅ The tone is still professional and helpful, following your original instructions

4. Now try looking up current regulations — a common need when taking on new legal matters:

   ```
   What are the filing deadlines for commercial litigation in Oregon?
   ```

   ```
   What are the latest changes to AML (Anti-Money Laundering) regulations for law firms?
   ```

   ```
   What are the recent updates to attorney-client privilege rules in federal courts?
   ```

   ```
   What are the current bar admission requirements for attorneys practicing in multiple states?
   ```

5. Compare this to Unit 1. Remember when you asked about specific policies and the agent gave generic answers? Try this:

   ```
   What are the recent key compliance considerations when onboarding a litigation client in Portland, Oregon?
   ```

   Now the agent can actually research and provide **current, location-specific regulatory information** rather than guessing.

6. Now try questions that **combine the agent's onboarding role with web research** — this is where the real value shows up for legal teams:

   ```
   I'm onboarding Nvidia as a new litigation client. What's been in the news about them recently that I should flag during intake?
   ```

   The agent should search Bing for recent Nvidia news (lawsuits, regulatory actions, earnings) and weave that into onboarding guidance — giving you a response that's both process-aware and factually current.

   ```
   We're taking on a new client in the cryptocurrency space. What are the latest SEC enforcement actions against crypto companies this year, and what compliance risks should I note during intake?
   ```

   Notice how the agent weaves together **its role as an onboarding agent** (what to collect, what steps to follow) with **real-time web knowledge** (recent news, current regulations, latest enforcement actions). This is the power of grounding — the agent isn't just a generic search engine, it's a legal intake assistant that can research.

7. Also try a question that *doesn't* need web search to see that the agent still behaves normally:

   ```
   What information do I need to collect from a new client during intake?
   ```

   The agent should still respond as your onboarding-agent — Bing Grounding doesn't replace the agent's core behavior, it **extends** it.

> **💡 Tip:** Pay attention to the citations in the agent's responses. Grounded answers will often include links or references to the web sources used. This transparency is critical in legal practice — you can verify the information before relying on it for client work.

> **📝 Note:** The agent is intelligent about when to use Bing. If you ask a general onboarding process question, it will rely on its instructions. If you ask about current events, regulations, or specific companies, it will search the web. This blending happens automatically.

---

## Summary

Congratulations! 🎉 You've added real-time web knowledge to your onboarding-agent. Here's what you accomplished:

| ✅ Done | ❌ Not Yet |
|---|---|
| Created a declarative agent in Foundry (Unit 1) | No firm-specific knowledge (policies, procedures) |
| Added Grounding with Bing for real-time web knowledge | No tools connected (e.g., matter tracker) |
| Agent can research clients and look up current regulations | No persistent state or memory |
| Agent cites its sources for transparency | No document understanding capabilities |

### Key Takeaway

Adding Bing Grounding to a declarative agent is **configuration, not code**. You didn't write any code, deploy any services, or modify any prompts. You simply connected a tool through the Foundry UI, and your agent immediately became more capable.

This pattern — extending agents through configuration — is a core principle of Foundry's declarative approach. As you'll see in the next units, the same pattern applies to knowledge sources, document processing, and external tools.

### What's Next

In **[Unit 3: Knowledge Grounding with Files](./unit-3-knowledge-grounding-files.md)**, we'll upload the firm's **Client Onboarding Handbook** so the agent can answer questions using your firm's actual policies and procedures — not just generic web results.

---

## Key Concepts

- **Grounding** — Connecting a language model to external data sources so its responses are based on real, verifiable information rather than just training data. Grounding reduces hallucination and improves accuracy.

- **Grounding with Bing** — An Azure service that enables AI agents to search the web via Bing and incorporate up-to-date search results into their responses. It provides real-time knowledge and source citations.

- **Hallucination** — When a language model generates information that sounds plausible but is factually incorrect. Grounding helps mitigate hallucination by giving the model access to authoritative sources.

- **Tools in Foundry** — Pluggable capabilities that can be added to a declarative agent through the Foundry UI. Grounding with Bing is one example; others include file uploads, MCP connections, and more.

- **Declarative Configuration** — The pattern of extending agent capabilities through UI-based configuration rather than writing code. This makes it fast to iterate and accessible to non-developers.

> **💡 Tip:** As you continue through the workshop, notice how each unit adds a new capability to the same agent — without rewriting what came before. This composability is what makes declarative agents so powerful.
