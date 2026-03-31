# Unit 1: Creating a Declarative Agent in Foundry

## Overview

Welcome to Unit 1 of the **Foundry Agents Essentials** workshop! In this unit, you'll create your very first AI agent using Microsoft Foundry — no code required.

A **declarative agent** in Foundry is configured entirely through the portal UI. Instead of writing code, you define the agent's behavior, instructions, and capabilities through a visual interface. Think of it like filling out a form that describes *what* your agent should do, rather than programming *how* it does it.

By the end of this unit, you'll have a working Client Onboarding Assistant that you can chat with in the Foundry playground. It won't be able to take actions in the real world yet — but it will serve as the foundation you build on in every subsequent unit.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Completed the infrastructure deployment (`azd up`) as described in the [main README](../README.md)
- ✅ Access to the Microsoft Foundry portal at [ai.azure.com](https://ai.azure.com)
- ✅ Azure credentials with the appropriate permissions to your deployed resource group

> **📝 Note:** If you haven't run `azd up` yet, go back to the root of this repository and follow the setup instructions in the README before continuing.

---

## What is a Declarative Agent?

There are two broad approaches to building AI agents:

| Approach | Description |
|---|---|
| **Declarative** | You *describe* the agent's behavior through configuration — its name, instructions, model, and connected tools. The platform handles the rest. |
| **Programmatic** | You *write code* that orchestrates the agent's behavior, managing conversation flow, tool calls, and state yourself. |

Declarative agents are a great starting point because they let you focus on **what the agent should do** without worrying about the underlying implementation. Microsoft Foundry makes this especially accessible — you can go from zero to a working agent in just a few minutes.

A declarative agent in Foundry has three core building blocks:

1. **Instructions** — A system prompt that defines the agent's persona and behavior
2. **Model** — The language model that powers the agent's responses
3. **Capabilities** — Optional extensions like knowledge sources and tools (we'll add these in later units)

> **💡 Tip:** Think of the instructions as the agent's "job description." The more specific and clear you are, the better the agent will perform.

---

## Steps

### Step 1: Navigate to Microsoft Foundry

1. Open your browser and go to [ai.azure.com](https://ai.azure.com).
2. Sign in with the same Azure credentials you used during infrastructure deployment.
3. Once signed in, you should see the Foundry portal home page.

> **📝 Note:** If this is your first time signing in, you may be prompted to select a directory or accept terms of service. Follow the on-screen prompts to continue.
>
> **💡 Tip:** The Foundry portal supports both a **New** and **Classic** experience. This lab requires the **Foundry (New)** experience. If you see a toggle or banner at the top of the portal offering to switch between New and Classic, make sure **Foundry (New)** is selected. The new experience is agent-centric and has all the features used in this lab.

---

### Step 2: Create a New Agent

Now let's create your first declarative agent.

1. From the Foundry home page, find and select the project that was created during your `azd up` deployment (it will be named **onboarding-lab**).
2. Select the **Build** tab on top-right. In the left-hand navigation, click on **Agents**.
3. Click the **Create Agent** button to start creating a new declarative agent.
4. Give your agent a name:

   ```
   Onboarding-Assistant
   ```

5. In the **Instructions** field, enter the following system prompt:

   ```
   You are a Client Onboarding Assistant for a professional services firm. You help team members onboard new clients and engagements by answering questions about onboarding procedures, collecting required information, and guiding them through each step of the process.

   When a user asks about onboarding a new client, help them gather the key details: client name, engagement type, a brief scope description, and primary contact information. Be professional, thorough, and concise.

   If the user asks about something outside of client onboarding, politely let them know your focus is on onboarding and offer to help with onboarding-related questions instead.
   ```

6. Leave the remaining settings at their defaults for now — we'll customize these in later units.
7. Click **Save** to save your new agent.

> **💡 Tip:** Good instructions are specific about what the agent *can* do and *how* it should respond. Notice we tell the agent to "be professional, thorough, and concise" — this sets the tone. We also define a scope boundary ("if the user asks about something outside of client onboarding"). In later units, we'll refine these instructions significantly.

---

### Step 3: Test Your Agent

With your agent created, let's take it for a spin in the Foundry playground.

1. After creating the agent, you should see a chat interface (the **playground**) on the right side of the screen.
2. Try sending a few messages to your agent. Here are some ideas:

   ```
   I need to onboard a new client. Where do I start?
   ```

   ```
   What information do I need to collect for a new construction management engagement?
   ```

   ```
   We have a new legal advisory client — Woodgrove Partners. Can you help me set up their engagement?
   ```

3. Observe the agent's responses. You should notice that:
   - ✅ The agent responds in a professional, helpful tone (following your instructions)
   - ✅ The agent *talks about* the onboarding process and asks clarifying questions
   - ❌ The agent **doesn't know your firm's actual policies** — it generates generic advice
   - ❌ The agent **cannot actually create onboarding records** — it can only generate text

> **📝 Note:** Right now, the agent is essentially "role-playing" as an onboarding assistant. It has no connected knowledge or tools, so it can only respond based on its model's general training data and your instructions. This is expected! We'll fix this in the upcoming units.

4. Try asking something outside the agent's declared scope:

   ```
   What's the weather in Seattle today?
   ```

   Notice how the agent responds — it should redirect you back to onboarding topics based on the boundary we set in the instructions. This is an early example of why clear instructions matter.

5. Now try a question that exposes the agent's current limitations:

   ```
   What is our firm's policy on conflict of interest checks during onboarding?
   ```

   The agent will give a reasonable-sounding but **generic** answer. It doesn't actually know your firm's specific policies — yet. In Unit 3, we'll upload the firm's onboarding handbook to fix this.

---

## Summary

Congratulations! 🎉 You've created your first declarative agent in Microsoft Foundry. Here's what you accomplished:

| ✅ Done | ❌ Not Yet |
|---|---|
| Created a declarative agent in Foundry | No external knowledge (e.g., web search) |
| Defined system instructions for agent behavior | No firm-specific knowledge (policies, procedures) |
| Tested the agent in the Foundry playground | No tools connected (e.g., project tracker) |
| Established scope boundaries | No persistent state or memory |

This baseline agent is the starting point for the rest of the workshop. In each subsequent unit, we'll add new capabilities to make the agent more powerful and useful.

### What's Next

In **[Unit 2: Grounding with Bing](./unit-2-grounding-with-bing.md)**, we'll add **Grounding with Bing Search** to give the agent access to real-time web information. This means it will be able to look up current regulations, industry news, and client company information — not just respond based on its training data.

---

## Key Concepts

- **Declarative Agent** — An agent defined through configuration (instructions, model, capabilities) rather than code. Foundry's UI lets you create these without any programming.

- **System Instructions (Agent Persona)** — The prompt that tells the agent who it is and how to behave. This is the most important part of a declarative agent's configuration.

- **Foundry Agent Playground** — The built-in chat interface in the Foundry portal where you can test and interact with your agents in real time.

- **Declarative vs. Programmatic Agents** — Declarative agents are configured through UI/config files; programmatic agents are built with code. Both have their place — declarative is great for rapid prototyping and simpler use cases, while programmatic gives you full control for complex scenarios.

> **💡 Tip:** As you continue through the workshop, keep your Foundry portal tab open. You'll be building on this same agent in every unit.
