# Unit 3: Knowledge Grounding with Files

## Overview

Welcome to Unit 3 of the **Foundry Agents Essentials** workshop! In this unit, you'll teach your agent something entirely new by uploading a **document as a knowledge source** — giving it domain-specific expertise that doesn't exist on the public web or in its training data.

Up to this point, your agent has a persona (Unit 1) and can search the web with Bing (Unit 2). But when you asked it about your firm's specific onboarding policies, it could only give generic advice. That changes now.

You'll upload **five Meridian Legal documents** — the Client Onboarding Handbook, a sample engagement proposal, a conflict-of-interest policy, a data retention policy, and a client retainer agreement template — in three different file formats (Markdown, PDF, and Word). After uploading, your agent will be able to answer detailed questions about your firm's specific procedures, approval workflows, pricing guidelines, and compliance requirements — with citations pointing back to the exact section of the document. It will even reason across multiple documents to connect information from different sources.

---

## Prerequisites

Before starting this unit, make sure you have:

- ✅ Completed [Unit 2: Grounding with Bing](./unit-2-grounding-with-bing.md)
- ✅ Your **onboarding-agent** is working in the Foundry playground with Bing Grounding configured
- ✅ Access to the [Microsoft Foundry portal](https://ai.azure.com)
- ✅ The sample documents from this repository:
  - [`docs/assets/firm-onboarding-handbook.md`](./assets/firm-onboarding-handbook.md) — Firm onboarding policies (Markdown)
  - [`docs/assets/sample-proposal.pdf`](./assets/sample-proposal.pdf) — MCO engagement proposal (PDF)
  - [`docs/assets/conflict-of-interest-policy.pdf`](./assets/conflict-of-interest-policy.pdf) — Conflict screening procedures (PDF)
  - [`docs/assets/client-retainer-agreement-template.docx`](./assets/client-retainer-agreement-template.docx) — Standard retainer agreement template (Word)
  - [`docs/assets/data-retention-policy.md`](./assets/data-retention-policy.md) — Data retention and destruction standards (Markdown)

> **📝 Note:** All five documents are included in this repository. You'll upload them directly to the Foundry portal in the steps below.

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

This approach is commonly known as **Retrieval-Augmented Generation (RAG)** — let's break down why it matters.

### What is RAG (Retrieval-Augmented Generation)?

Large language models are trained on massive amounts of public text, but they don't *know* your firm's policies, your client agreements, or your internal procedures. They also can't learn new information after their training cutoff. RAG solves both problems by adding a **retrieval step** before the model generates a response.

Here's the core idea:

```
                    ┌──────────────┐
  User question ──▶ │   Retrieve   │ ──▶ Relevant passages from your documents
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Augment    │ ──▶ Combine the question + retrieved passages
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Generate   │ ──▶ Model produces a grounded, cited answer
                    └──────────────┘
```

**Without RAG**, the model answers from memory — which means generic advice, outdated information, or outright hallucinations about your firm's specific policies.

**With RAG**, the model first searches your documents for relevant passages, then uses those passages as context to generate an accurate, specific answer. It's the difference between asking someone who *read about* law firms in general versus someone who *has your firm's handbook open on their desk*.

Why this matters for legal practice:

| Without RAG | With RAG |
|-------------|----------|
| "Typically, law firms require partner approval for high-value engagements." | "Per Section 6 of your handbook, engagements between $100,000 and $500,000 require Managing Partner approval." |
| Generic, potentially wrong | Specific, cited, verifiable |

When you upload files to your agent in the next steps, Foundry handles the entire RAG pipeline automatically — chunking your documents, creating vector embeddings, storing them in a searchable index, and wiring up the retrieval at query time. You get production-grade RAG without writing a single line of code.

> **💡 Tip:** Think of this as giving your agent a reference manual. When someone asks a policy question, the agent looks up the answer in the manual rather than guessing. Just like a well-trained employee would.

### Why Files vs. Web Search?

| Source | Best For | Example |
|--------|----------|---------|
| **Bing (Web)** | Public, current information | "What are the latest AML regulations for law firms?" |
| **Files (Documents)** | Private, firm-specific knowledge | "What is our approval workflow for matters over $100,000?" |

Your agent will now have both — it can search the web for public information *and* reference your internal documents for firm-specific questions. The agent intelligently decides which source to use based on the question.

---

## Steps

### Step 1: Review the Sample Documents

Before uploading, let's take a quick look at the documents you'll be giving to your agent. You have **five documents** in three different file formats — giving you a realistic multi-document knowledge base.

1. Open the file [`docs/assets/firm-onboarding-handbook.md`](./assets/firm-onboarding-handbook.md) in this repository.
2. Skim through the content. You'll see it covers:
   - The five-stage onboarding lifecycle (Intake → Due Diligence → Scope & Proposal → Approval → Activation)
   - Required intake information and document collection
   - Conflict of interest and AML screening procedures
   - Pricing guidelines by engagement type
   - Approval authority levels based on engagement value
   - Client communication standards
   - Data protection and confidentiality policies
   - Escalation procedures

3. Review the other four documents briefly:

   | Document | Format | Key Content |
   |----------|--------|-------------|
   | [`sample-proposal.pdf`](./assets/sample-proposal.pdf) | PDF | MCO engagement proposal with scope, fees, and timeline |
   | [`conflict-of-interest-policy.pdf`](./assets/conflict-of-interest-policy.pdf) | PDF | Conflict screening procedures, ethical walls, resolution workflows |
   | [`client-retainer-agreement-template.docx`](./assets/client-retainer-agreement-template.docx) | Word | Standard retainer agreement with fee structures and terms |
   | [`data-retention-policy.md`](./assets/data-retention-policy.md) | Markdown | Data retention schedules, legal holds, destruction procedures |

> **📝 Note:** These are realistic but fictional documents for Meridian Legal. They cover the kinds of policies that law firms typically maintain. In a real scenario, you would upload your actual firm's documents.

---

### Step 2: Upload the Documents to Your Agent

Now let's give this knowledge to your onboarding-agent. You'll upload all five documents at once.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) and navigate to your project.
2. Select the **Build** tab on top-right. In the left-hand navigation, click on **Agents**.
3. Select the **onboarding-agent** agent to open its configuration.
4. Scroll down to the **Knowledge** section of the agent configuration.
5. Click **Add** and select **Files**.
6. Foundry will prompt you to upload files:
   - Click **Upload files** and select **all five documents** from the `docs/assets/` folder in this repository:
     - `firm-onboarding-handbook.md`
     - `sample-proposal.pdf`
     - `conflict-of-interest-policy.pdf`
     - `client-retainer-agreement-template.docx`
     - `data-retention-policy.md`
   - Wait for the uploads to complete. Foundry will create a **vector store** and index the document content.
7. Once all files are uploaded and indexed, you should see them listed under the Knowledge section with a status indicating they have been processed.
8. **Save** your agent configuration.

> **💡 Tip:** Foundry supports multiple file formats including PDF, Markdown, Word (.docx), and plain text. Notice how you're uploading three different formats — Foundry handles them all seamlessly. For best results, use well-structured documents with clear headings and sections — this helps the retrieval system find the most relevant passages.

> **📝 Note:** Processing the documents may take a minute or two depending on their size. You can proceed to testing once the status shows all files have been successfully indexed.

---

### Step 3: Update the Instructions to Use Knowledge Only

Now that your agent has firm-specific documents, let's update its instructions so it **only answers firm-specific questions from its uploaded knowledge** — not from its general training data. This is critical for legal practice: you don't want the agent inventing policies or mixing generic advice with your firm's actual procedures.

At the same time, the agent still has Bing grounding from Unit 2. We want to preserve that — external lookups for regulations, court filings, and public information are valuable. The guardrail is specifically about **firm-internal questions**.

1. In the Foundry portal, open the **onboarding-agent** configuration.
2. In the **Instructions** field, replace the existing instructions with:

   ```
   You are a Client Onboarding Agent for Meridian Legal. You help team members onboard new clients and matters by answering questions about intake procedures, firm policies, and engagement requirements.

   **Important:** For any question about firm policies, procedures, or internal processes, only use information from the uploaded firm documents. Do not rely on your general training knowledge for firm-specific answers. If the answer is not found in the provided documents, say so clearly — do not guess or fill in with generic advice. Always cite which document or section your answer comes from.

   You may still use Bing search to look up external information such as current regulations, public filings, court rules, or industry standards. When a question combines internal firm requirements with external information, clearly separate what comes from firm documents versus what comes from web search.

   When a user asks about onboarding a new client, help them gather the key details: client name, matter type, a brief scope description, and primary contact information. Be professional, thorough, and concise.
   ```

3. **Save** your agent configuration.

> **💡 Tip:** Notice the guardrail is scoped to **firm-internal questions** — not all questions. This preserves the Bing grounding from Unit 2 for external lookups (regulations, filings, public records) while ensuring the agent never fabricates firm policies. For legal work, this distinction matters: you want the agent to say "I don't have that in our documents" rather than making up a retention schedule, but you still want it to look up current Oregon filing deadlines.

---

### Step 4: Test the Knowledge-Grounded Agent

Now let's see the dramatic difference that firm-specific knowledge makes. You'll ask questions that produced generic answers in Unit 1 — but this time, the agent has your firm's documents.

1. In the Foundry portal, open the **playground** for your onboarding-agent.
2. Start with a question about your firm's specific onboarding process:

   ```
   What are the stages of our client onboarding process?
   ```

3. Observe the response carefully. You should notice:
   - ✅ The agent describes the **five specific stages** from your handbook (Intake, Due Diligence, Scope & Proposal, Approval, Activation)
   - ✅ The response includes **specific details** like target durations and responsible parties
   - ✅ The agent **cites the document** — you may see references indicating which section the information came from

4. Now try questions about specific policies — starting with legal-oriented questions:

   ```
   Can we start work with a client before the NDA is signed?
   ```

   The agent should reference the FAQ section and explain that an NDA must be signed before any substantive work begins, though preliminary discussions are permitted.

   ```
   What are the AML screening requirements for high-value engagements?
   ```

   ```
   What is the conflict of interest screening process for new litigation matters?
   ```

   ```
   What are the data retention and confidentiality requirements when we close out a legal engagement?
   ```

5. Try more policy-specific questions across different practice areas:

   ```
   Who needs to approve an engagement worth $200,000?
   ```

   The agent should tell you that engagements between $100,000 and $500,000 require **Managing Partner** approval — a specific detail from Section 6 of the handbook.

   ```
   What is the maximum response time for a client's initial inquiry?
   ```

   ```
   What additional compliance checks are needed for litigation matters?
   ```

6. Now combine web knowledge with document knowledge:

   ```
   A litigation client in Portland needs us to review regulatory filings. What are our firm's requirements for this, and what are the current Oregon filing regulations?
   ```

   Watch how the agent **blends both knowledge sources** — pulling firm-specific procedures from the handbook and current regulatory information from Bing. This is the power of having multiple knowledge sources working together.

> **💡 Tip:** Pay attention to the **citations** in the agent's responses. When the agent references the uploaded documents, you'll see indicators showing which sections it pulled information from. This is essential for trust — especially in legal practice where accuracy matters.

> **📝 Note:** The agent uses the documents as a preferred source for firm-specific questions, but it won't force-fit document content where it doesn't apply. If you ask a general knowledge question (like "What's in the news today?"), the agent will use Bing instead.

---

### Step 5: Test Cross-Document Reasoning

This is where having **multiple documents** really shines. Let's test your agent with questions that require information from **multiple** documents — spanning policies, proposals, and templates across different file formats.

1. Start with a question that requires cross-document reasoning — combining the proposal's engagement value with the handbook's approval thresholds:

   ```
   What is the estimated engagement value for the MCO matter and what approval level does that require?
   ```

   The agent should identify that the MCO engagement is valued at **$150,000** (from the proposal) and that engagements between $100,000 and $500,000 require **Managing Partner** approval (from the handbook's Section 6). Watch how the agent connects information from both documents seamlessly.

2. Try a question that compares billing approaches across multiple documents:

   ```
   Compare the billing model proposed for MCO against our standard litigation rates and our retainer agreement template terms.
   ```

   The agent should reference the proposal's billing model (monthly invoicing based on hours worked), the handbook's pricing guidelines for litigation ($300-$500/hour), and the retainer agreement template's fee structure options (hourly, fixed fee, evergreen retainer). Notice how it reasons across a markdown file and a Word document to build a comprehensive answer.

3. Test a conflict-of-interest question that draws from the PDF document:

   ```
   MCO has a prior engagement with our firm. What conflict screening steps are required before we proceed with this new matter?
   ```

   The agent should pull from the **conflict-of-interest-policy.pdf** to describe the mandatory screening process — checking the centralized database, identifying all adverse parties, and noting that prior engagements require rescreening.

4. Ask a question that spans the data retention policy and the engagement:

   ```
   Once the MCO matter closes, how long do we need to retain the case files and what destruction procedures apply?
   ```

   The agent should reference the **data-retention-policy.md** — litigation matter files are retained for **10 years after final disposition**, and destruction requires Practice Director approval, cross-cut shredding for physical documents, and a Certificate of Destruction.

5. Try a compliance question that requires reasoning across multiple policies:

   ```
   If a potential conflict is identified during the MCO engagement, what happens to the data and documents while the Ethics Committee reviews it? Can anything be destroyed?
   ```

   The agent should connect the conflict resolution procedures (from the conflict policy — Ethics Committee has 3 business days to determine) with the legal hold requirements (from the data retention policy — legal holds suspend all destruction schedules). This requires reasoning across the PDF and markdown policies simultaneously.

6. Test the retainer agreement template knowledge:

   ```
   What are the standard payment terms for client invoices and what happens with late payments?
   ```

   The agent should cite the retainer agreement template: invoices are due **Net 30 days**, late payments accrue interest at **1.5% per month**, and expenses exceeding $2,500/month require prior client approval.

7. Try the full approval workflow:

   ```
   Based on the MCO engagement value, who needs to sign off and what's the approval checklist?
   ```

   The agent should combine the $150,000 engagement value (proposal) with the approval authority table and criteria checklist from the handbook (Section 6) to walk through the complete approval process.

8. Verify that **web-grounded questions** still work alongside the expanded knowledge:

   ```
   MCO operates in food manufacturing. Have there been any FDA food-safety enforcement actions or warning letters issued to food manufacturers in 2026? How would that affect our engagement scope?
   ```

   The agent should use Bing to look up recent FDA enforcement actions (the model can't know 2026 events from training data), then reference the engagement scope from the proposal to explain how regulatory compliance review would apply.

9. Finally, try a complex question that blends all sources:

    ```
    MCO's supplier in Portland just received an FDA warning letter this year for food-safety violations.
    What does our engagement scope cover for regulatory compliance work, what's our standard billing
    rate for regulatory matters, and how long would we retain the regulatory analysis files?
    ```

    Watch the agent pull from the proposal (regulatory compliance review scope), the handbook (regulatory compliance rate range of $275-$500/hour), and the data retention policy (regulatory compliance files retained for 10 years). The mention of a current FDA warning letter should also trigger Bing to look up recent FDA enforcement activity.

> **💡 Tip:** Cross-document reasoning is one of the most powerful capabilities of file-based grounding. Notice that the agent handled PDF, Word, and Markdown files seamlessly — it doesn't matter what format a document was in; once it's indexed, the vector store treats all content the same way.

---

### Step 6: Explore Edge Cases

Let's see how the agent handles questions that push the boundaries of its knowledge.

1. Ask about something **not in any of the documents**:

   ```
   What is our firm's remote work policy?
   ```

   The agent should acknowledge that this isn't covered in the available documentation and may suggest you check with the appropriate team.

2. Try a question that **tests the agent's ability to find specific numbers**:

   ```
   What is the standard hourly rate range for litigation support?
   ```

   The agent should cite $300–$500/hour from the pricing guidelines in Section 5 of the handbook.

3. Ask a question that **combines document knowledge with reasoning**:

   ```
   We're onboarding a corporate client with an estimated matter value of $75,000. Walk me through the full approval process step by step.
   ```

   The agent should reference the approval thresholds from the handbook ($25,000–$100,000 requires Practice Director approval) and combine this with the general onboarding workflow.

---

## Summary

Congratulations! 🎉 You've transformed your agent from a generic chatbot into a firm-specific knowledge expert with **multi-document reasoning** capabilities. Here's what you've accomplished:

| ✅ Done | ❌ Not Yet |
|---|---|
| Created a declarative agent in Foundry (Unit 1) | No structured conversational flow |
| Added Grounding with Bing for real-time web knowledge (Unit 2) | No tools connected (e.g., matter tracker) |
| Added file-based knowledge grounding with five firm documents (Unit 3) | No document understanding / field extraction |
| Agent answers firm-specific policy questions with citations | No structured onboarding workflow |
| Agent reasons across multiple documents in different formats | |
| Agent blends web and document knowledge intelligently | |

### Key Takeaway

Knowledge Grounding with Files turns your agent into a **legal domain expert**. Instead of generic AI responses, your agent now gives answers grounded in your firm's actual policies and procedures — with citations. By uploading multiple documents in different formats (Markdown, PDF, Word), you've given your agent a comprehensive knowledge base that supports cross-document reasoning. This is the foundation for trustworthy AI in legal practice, where accuracy and compliance are non-negotiable.

The combination of **web grounding** (Bing) and **document grounding** (files) gives your agent two complementary knowledge sources: one for public, current information and one for private, firm-specific knowledge.

### What's Next

In **[Unit 4: Instructions & Conversational Flow](./unit-4-instructions-and-flow.md)**, we'll redesign the agent's instructions to guide users through a structured legal intake workflow — turning it from a Q&A assistant into a process-driven intake specialist.

---

## Key Concepts

- **Knowledge Grounding with Files** — Uploading documents to a Foundry agent so it can reference them when answering questions. The agent retrieves relevant passages from the indexed documents and uses them to generate accurate, cited responses.

- **Retrieval-Augmented Generation (RAG)** — A pattern where the AI model first *retrieves* relevant information from a knowledge source, then *generates* a response using that information. This dramatically improves accuracy for domain-specific questions.

- **Vector Store** — The indexed, searchable representation of your uploaded documents. Foundry creates this automatically when you upload files. The vector store enables fast, semantic search across your document content.

- **Citations** — References in the agent's response that point back to the specific document sections used to generate the answer. Citations build trust and allow users to verify information.

- **Knowledge vs. Tools** — Knowledge sources (files, Bing) provide information the agent incorporates into its responses. Tools (MCP endpoints, functions) allow the agent to take actions. Your agent currently has knowledge sources; in later units, we'll add tools.

- **Cross-Document Reasoning** — The ability of an agent to combine information from multiple uploaded documents in a single response. By uploading several documents covering different aspects of your firm's operations, the agent can connect details from a client proposal with policies from an internal handbook, or link conflict procedures with data retention requirements.

> **💡 Tip:** In a real-world deployment, you'd upload your actual firm documents — intake procedures, compliance guides, fee schedules, engagement letter templates, and more. The more comprehensive the knowledge base, the more useful the agent becomes.
