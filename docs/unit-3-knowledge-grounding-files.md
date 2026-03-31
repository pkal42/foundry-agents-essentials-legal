# Unit 3: Knowledge Grounding with Files

## Overview

Welcome to Unit 3 of the **Foundry Agents Essentials** workshop! In this unit, you'll teach your agent something entirely new by uploading a **document as a knowledge source** — giving it domain-specific expertise that doesn't exist on the public web or in its training data.

Up to this point, your agent has a persona (Unit 1) and can search the web with Bing (Unit 2). But when you asked it about your firm's specific onboarding policies, it could only give generic advice. That changes now.

You'll upload the **Meridian Professional Services Client Onboarding Handbook** — a realistic firm policy document included in this repository. After uploading, your agent will be able to answer detailed questions about your firm's specific procedures, approval workflows, pricing guidelines, and compliance requirements — with citations pointing back to the exact section of the document.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Completed [Unit 2: Grounding with Bing](./unit-2-grounding-with-bing.md)
- ✅ Your **Onboarding-Assistant** is working in the Foundry playground with Bing Grounding configured
- ✅ Access to the [Microsoft Foundry portal](https://ai.azure.com)
- ✅ The sample document: [`docs/sample-documents/firm-onboarding-handbook.md`](./sample-documents/firm-onboarding-handbook.md)

> **📝 Note:** The onboarding handbook is included in this repository. You'll upload it directly to the Foundry portal in the steps below.

---

## What is Knowledge Grounding with Files?

In Unit 2, you added Bing to give your agent access to public web information. But what about **private, internal knowledge** — like your firm's policies, procedures, and guidelines?

**Knowledge Grounding with Files** lets you upload documents directly to your agent. Foundry processes these files, indexes their content, and makes them available for the agent to reference when answering questions. The agent treats the uploaded files as an authoritative knowledge source — meaning it will prefer information from your documents over generic responses.

Here's how it works:

1. **Upload** — You provide one or more files (PDF, Markdown, Word, etc.) through the Foundry portal
2. **Index** — Foundry processes and indexes the document content into a searchable vector store
3. **Retrieve** — When the agent receives a question, it searches the indexed content for relevant passages
4. **Generate** — The agent uses the retrieved passages to craft an accurate, grounded response
5. **Cite** — The response includes references to the specific document sections used

This approach is commonly known as **Retrieval-Augmented Generation (RAG)** — the agent retrieves relevant information before generating a response, dramatically improving accuracy for domain-specific questions.

> **💡 Tip:** Think of this as giving your agent a reference manual. When someone asks a policy question, the agent looks up the answer in the manual rather than guessing. Just like a well-trained employee would.

### Why Files vs. Web Search?

| Source | Best For | Example |
|--------|----------|---------|
| **Bing (Web)** | Public, current information | "What are the latest OSHA requirements?" |
| **Files (Documents)** | Private, firm-specific knowledge | "What is our approval workflow for engagements over $100,000?" |

Your agent now has both — it can search the web for public information *and* reference your internal documents for firm-specific questions. The agent intelligently decides which source to use based on the question.

---

## Steps

### Step 1: Review the Sample Document

Before uploading, let's take a quick look at the document you'll be giving to your agent.

1. Open the file [`docs/sample-documents/firm-onboarding-handbook.md`](./sample-documents/firm-onboarding-handbook.md) in this repository.
2. Skim through the content. You'll see it covers:
   - The five-stage onboarding lifecycle (Intake → Due Diligence → Scope & Proposal → Approval → Activation)
   - Required intake information and document collection
   - Conflict of interest and AML screening procedures
   - Pricing guidelines by engagement type
   - Approval authority levels based on engagement value
   - Client communication standards
   - Data protection and confidentiality policies
   - Escalation procedures

> **📝 Note:** This is a realistic but fictional document for Meridian Professional Services. It's designed to cover the kinds of policies that legal, construction, and consulting firms typically maintain. In a real scenario, you would upload your actual firm's onboarding documents.

---

### Step 2: Upload the Document to Your Agent

Now let's give this knowledge to your Onboarding Assistant.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) and navigate to your project.
2. Select the **Build** tab on top-right. In the left-hand navigation, click on **Agents**.
3. Select the **Onboarding-Assistant** agent to open its configuration.
4. Scroll down to the **Knowledge** section of the agent configuration.
5. Click **Add** and select **Files**.
6. Foundry will prompt you to upload files:
   - Click **Upload files** and select the `firm-onboarding-handbook.md` file from the `docs/sample-documents/` folder in this repository.
   - Wait for the upload to complete. Foundry will create a **vector store** and index the document content.
7. Once the file is uploaded and indexed, you should see it listed under the Knowledge section with a status indicating it has been processed.
8. **Save** your agent configuration.

> **💡 Tip:** Foundry supports multiple file formats including PDF, Markdown, Word (.docx), and plain text. For best results, use well-structured documents with clear headings and sections — this helps the retrieval system find the most relevant passages.

> **📝 Note:** Processing the document may take a minute or two depending on its size. You can proceed to testing once the status shows the file has been successfully indexed.

---

### Step 3: Test the Knowledge-Grounded Agent

Now let's see the dramatic difference that firm-specific knowledge makes. You'll ask the same kinds of questions that produced generic answers in Unit 1 — but this time, the agent has your handbook.

1. In the Foundry portal, open the **playground** for your Onboarding-Assistant.
2. Start with a question about your firm's specific onboarding process:

   ```
   What are the stages of our client onboarding process?
   ```

3. Observe the response carefully. You should notice:
   - ✅ The agent describes the **five specific stages** from your handbook (Intake, Due Diligence, Scope & Proposal, Approval, Activation)
   - ✅ The response includes **specific details** like target durations and responsible parties
   - ✅ The agent **cites the document** — you may see references indicating which section the information came from

4. Now try questions about specific policies:

   ```
   Who needs to approve an engagement worth $200,000?
   ```

   The agent should tell you that engagements between $100,000 and $500,000 require **Managing Partner** approval — a specific detail from Section 6 of the handbook.

5. Try more policy-specific questions:

   ```
   What are the AML screening requirements for high-value engagements?
   ```

   ```
   What is the maximum response time for a client's initial inquiry?
   ```

   ```
   What additional compliance checks are needed for construction clients?
   ```

6. Now combine web knowledge with document knowledge:

   ```
   A construction client in Portland wants to engage us for permit coordination. What are our firm's requirements for this, and what are the current Portland building permit regulations?
   ```

   Watch how the agent **blends both knowledge sources** — pulling firm-specific procedures from the handbook and current regulatory information from Bing. This is the power of having multiple knowledge sources working together.

7. Finally, test with a question that the handbook explicitly answers:

   ```
   Can we start work with a client before the NDA is signed?
   ```

   The agent should reference the FAQ section and explain that an NDA must be signed before any substantive work begins, though preliminary discussions are permitted.

> **💡 Tip:** Pay attention to the **citations** in the agent's responses. When the agent references the uploaded document, you'll see indicators showing which sections it pulled information from. This is essential for trust — especially in professional services where accuracy matters.

> **📝 Note:** The agent uses the document as a preferred source for firm-specific questions, but it won't force-fit document content where it doesn't apply. If you ask a general knowledge question (like "What's in the news today?"), the agent will use Bing instead.

---

### Step 4: Explore Edge Cases

Let's see how the agent handles questions that push the boundaries of its knowledge.

1. Ask about something **not in the handbook**:

   ```
   What is our firm's remote work policy?
   ```

   The agent should acknowledge that this isn't covered in the available documentation and may suggest you check with the appropriate team.

2. Ask a question that **combines handbook knowledge with reasoning**:

   ```
   We're onboarding a consulting client with an estimated engagement value of $75,000. Walk me through the full approval process step by step.
   ```

   The agent should reference the approval thresholds from the handbook ($25,000–$100,000 requires Practice Director approval) and combine this with the general onboarding workflow.

3. Try a question that **tests the agent's ability to find specific numbers**:

   ```
   What is the standard hourly rate range for litigation support?
   ```

   The agent should cite $300–$500/hour from the pricing guidelines in Section 5 of the handbook.

---

## Summary

Congratulations! 🎉 You've transformed your agent from a generic chatbot into a firm-specific knowledge expert. Here's what you've accomplished:

| ✅ Done | ❌ Not Yet |
|---|---|
| Created a declarative agent in Foundry (Unit 1) | No multi-source knowledge bases |
| Added Grounding with Bing for real-time web knowledge (Unit 2) | No document understanding / field extraction |
| Added file-based knowledge grounding with firm handbook (Unit 3) | No tools connected (e.g., project tracker) |
| Agent answers firm-specific policy questions with citations | No structured onboarding workflow |
| Agent blends web and document knowledge intelligently | |

### Key Takeaway

Knowledge Grounding with Files turns your agent into a **domain expert**. Instead of generic AI responses, your agent now gives answers grounded in your firm's actual policies and procedures — with citations. This is the foundation for trustworthy AI in professional services, where accuracy and compliance are non-negotiable.

The combination of **web grounding** (Bing) and **document grounding** (files) gives your agent two complementary knowledge sources: one for public, current information and one for private, firm-specific knowledge.

### What's Next

In **[Unit 4: Knowledge Bases with Multiple Sources](./unit-4-knowledge-bases.md)**, we'll go beyond single-file uploads and create a **knowledge base** that combines multiple sources — files, Azure AI Search indexes, and more — giving your agent access to a richer, more comprehensive set of firm knowledge.

---

## Key Concepts

- **Knowledge Grounding with Files** — Uploading documents to a Foundry agent so it can reference them when answering questions. The agent retrieves relevant passages from the indexed documents and uses them to generate accurate, cited responses.

- **Retrieval-Augmented Generation (RAG)** — A pattern where the AI model first *retrieves* relevant information from a knowledge source, then *generates* a response using that information. This dramatically improves accuracy for domain-specific questions.

- **Vector Store** — The indexed, searchable representation of your uploaded documents. Foundry creates this automatically when you upload files. The vector store enables fast, semantic search across your document content.

- **Citations** — References in the agent's response that point back to the specific document sections used to generate the answer. Citations build trust and allow users to verify information.

- **Knowledge vs. Tools** — Knowledge sources (files, Bing) provide information the agent incorporates into its responses. Tools (MCP endpoints, functions) allow the agent to take actions. Your agent currently has knowledge sources; in later units, we'll add tools.

> **💡 Tip:** In a real-world deployment, you'd upload your actual firm documents — employee handbooks, compliance guides, service catalogs, standard operating procedures, and more. The more comprehensive the knowledge base, the more useful the agent becomes.
