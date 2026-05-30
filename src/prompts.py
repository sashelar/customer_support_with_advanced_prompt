"""
Prompt Engineering Templates for Customer Support Automation
This module contains all the prompt templates used for various customer support tasks.
"""

# System prompt for the customer support assistant
SYSTEM_PROMPT = """You are an AI assistant for "FreshCart", an online food & grocery delivery platform.
Your role is to help analyze and respond to customer support requests professionally and efficiently.
Always be polite, empathetic, and solution-oriented in your responses."""

# ============================
# 1. CATEGORIZATION PROMPTS
# ============================

CATEGORIZATION_PROMPT = """Analyze the following customer request and categorize it into ONE of these categories:
- GENERIC_INQUIRY: General questions about the service, app usage, or account
- REFUND_REQUEST: Customer wants a refund or compensation
- ORDER_STATUS: Questions about order tracking, delivery time, or order issues
- POLICY_QUERY: Questions about policies (return, refund, delivery, payment)
- COMPLAINT: Customer is expressing dissatisfaction or reporting a problem

Customer Request: {customer_message}

Respond ONLY with the category name and a brief 1-sentence explanation.
Format: CATEGORY | Explanation"""

# ============================
# 2. GENERIC INQUIRY HANDLING
# ============================

GENERIC_INQUIRY_PROMPT = """You are handling a general customer inquiry for FreshCart.

Customer Question: {customer_message}

Provide a helpful, friendly response that:
1. Directly answers their question
2. Provides any relevant additional information
3. Guides them to next steps if applicable
4. Keeps the tone warm and professional

Response:"""

# ============================
# 3. REFUND REQUEST HANDLING
# ============================

REFUND_REQUEST_PROMPT = """A customer is requesting a refund or compensation.

Customer Request: {customer_message}
Order Details: {order_details}

Based on FreshCart's refund policy:
- Damaged/spoiled items: Full refund or replacement
- Missing items: Refund for missing items only
- Late delivery (>30 min): 20% discount voucher
- Quality issues: Case-by-case evaluation

Provide a response that:
1. Shows empathy for their situation
2. Explains the applicable policy clearly
3. Offers a specific solution (refund amount, voucher, or next steps)
4. Asks for any additional information needed

Response:"""

# ============================
# 4. ORDER STATUS HANDLING
# ============================

ORDER_STATUS_PROMPT = """Customer is inquiring about their order status.

Customer Message: {customer_message}
Order Information: {order_info}

Provide an update that:
1. Clearly states the current order status
2. Provides estimated delivery time if applicable
3. Explains any delays or issues proactively
4. Offers assistance if there's a problem

Response:"""

# ============================
# 5. POLICY QUERY HANDLING
# ============================

POLICY_QUERY_PROMPT = """Customer is asking about FreshCart policies.

Customer Question: {customer_message}

Relevant Policy Context: {policy_context}

Provide a clear response that:
1. Explains the policy in simple, understandable terms
2. Highlights key points that address their specific question
3. Provides examples if it helps clarify
4. Mentions where they can find full policy details

Response:"""

# ============================
# 6. COMPLAINT HANDLING
# ============================

COMPLAINT_HANDLING_PROMPT = """A customer has filed a complaint or is expressing dissatisfaction.

Customer Complaint: {customer_message}
Issue Type: {issue_type}

Provide an empathetic response that:
1. Acknowledges their frustration and apologizes sincerely
2. Shows you understand the specific issue
3. Explains what went wrong (if known)
4. Offers a concrete solution or compensation
5. Assures them of steps to prevent recurrence
6. Provides a direct escalation path if needed

Response:"""

# ============================
# 7. GUARDRAILS PROMPT
# ============================

GUARDRAILS_PROMPT = """You are a safety and compliance checker for customer support responses.

Analyze this response for the following issues:

Response to Check: {response}

Check for:
1. TOXIC_LANGUAGE: Any rude, offensive, or unprofessional language
2. PII_EXPOSURE: Exposure of personal information (emails, phone numbers, addresses, credit card numbers)
3. POLICY_VIOLATION: Promises or commitments outside company policy
4. DISCRIMINATORY_CONTENT: Any biased or discriminatory language
5. UNSAFE_ADVICE: Advice that could harm the customer or business

Respond in this exact format:
SAFE: YES/NO
ISSUES: [List any issues found, or "None"]
EXPLANATION: [Brief explanation]
CORRECTED_RESPONSE: [If unsafe, provide a corrected version]"""

# ============================
# 8. LLM-AS-A-JUDGE EVALUATION
# ============================

JUDGE_EVALUATION_PROMPT = """You are an expert evaluator of customer support responses.

Evaluate the following AI-generated response across these dimensions:

Original Customer Request: {customer_message}
AI Response: {ai_response}

Rate each dimension from 1-5 (5 being best) and provide justification:

1. RELEVANCE: Does the response directly address the customer's request?
2. CLARITY: Is the response clear, well-structured, and easy to understand?
3. EMPATHY: Does the response show appropriate empathy and professionalism?
4. COMPLETENESS: Does it provide all necessary information?
5. ACTIONABILITY: Does it give clear next steps or solutions?

Provide ratings in this format:
RELEVANCE: [score] - [justification]
CLARITY: [score] - [justification]
EMPATHY: [score] - [justification]
COMPLETENESS: [score] - [justification]
ACTIONABILITY: [score] - [justification]
OVERALL_SCORE: [average score]
RECOMMENDATION: APPROVE/REVISE/REJECT"""

# Sample data for testing
SAMPLE_ORDERS = {
    "ORD123": {
        "status": "In Transit",
        "items": ["Organic Apples 1kg", "Fresh Milk 2L", "Whole Wheat Bread"],
        "estimated_delivery": "Today, 6:30 PM",
        "total": "$24.99"
    },
    "ORD456": {
        "status": "Delayed",
        "items": ["Mixed Vegetables Pack", "Chicken Breast 500g"],
        "estimated_delivery": "Tomorrow, 10:00 AM",
        "total": "$18.50",
        "delay_reason": "High demand in your area"
    }
}

# ============================
# MLS 3 - CASE STUDY 1: SUPPORT TICKET CLASSIFICATION
# ============================

TICKET_ZERO_SHOT_V1 = """
Classify customer support messages into one of these categories:
1) Incident: Unexpected issue requiring immediate attention
2) Request: Routine inquiry or service request
3) Problem: Underlying issue causing multiple incidents
4) Change: Planned change or update
"""

TICKET_ZERO_SHOT_V2 = """
You are an enterprise-grade ticket classification engine.
Classify customer support messages into one of these categories based on their content and intent:

1) Incident: Unexpected technical or billing issue requiring immediate resolution.
   - Payment processing failures
   - Duplicate charges
   - System access problems
   - Recent errors affecting service

2) Request: Inquiry about products/services or standard information needs.
   - Pricing/plan questions
   - Payment method inquiries
   - Feature explanations
   - Discount/offer requests

3) Problem: Recurring or systemic issue causing multiple incidents.
   - Persistent billing discrepancies
   - Chronic integration failures
   - Ongoing synchronization issues
   - Patterns of incorrect charges

4) Change: Modification to existing account or service configuration.
   - Billing detail updates
   - Payment method changes
   - Subscription modifications
   - System integration updates

Respond ONLY with the exact category name (Incident / Request / Problem / Change).
Do not explain your reasoning.
"""

TICKET_FEW_SHOT_SYSTEM = """
Classify customer support messages into one of these categories based on their content and intent:

1) Incident: Unexpected technical or billing issue requiring immediate resolution.
   - Payment processing failures
   - Duplicate charges
   - System access problems
   - Recent errors affecting service

2) Request: Inquiry about products/services or standard information needs.
   - Pricing/plan questions
   - Payment method inquiries
   - Feature explanations
   - Discount/offer requests

3) Problem: Recurring or systemic issue causing multiple incidents.
   - Persistent billing discrepancies
   - Chronic integration failures
   - Ongoing synchronization issues
   - Patterns of incorrect charges

4) Change: Modification to existing account or service configuration.
   - Billing detail updates
   - Payment method changes
   - Subscription modifications
   - System integration updates

Respond ONLY with the exact category name.
Do not explain your reasoning.
"""

# Few-shot examples (1 per category for 4-shot; can pick 1 for 1-shot)
TICKET_FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "We're getting a 'payment declined' error on our checkout page since this morning. No transactions are going through."},
    {"role": "assistant", "content": "Incident"},
    {"role": "user", "content": "Could you explain the difference between your Basic and Pro subscription plans?"},
    {"role": "assistant", "content": "Request"},
    {"role": "user", "content": "Our monthly invoices have been showing incorrect amounts for the past three months due to a billing sync error."},
    {"role": "assistant", "content": "Problem"},
    {"role": "user", "content": "We need to update our credit card on file and switch billing from monthly to annual."},
    {"role": "assistant", "content": "Change"},
]

SAMPLE_SUPPORT_TICKETS = {
    "Incident – Payment Failure": "Our payment gateway stopped processing transactions 20 minutes ago. Customers are unable to check out.",
    "Request – Pricing Info": "Can you tell me what features are included in the Enterprise plan and how it's priced?",
    "Problem – Recurring Billing Bug": "For the last four billing cycles we have been charged twice each month. This keeps happening despite multiple reports.",
    "Change – Update Card Details": "I'd like to change the credit card associated with our account to a new corporate card.",
    "Incident – Login Error": "Since the last update, none of our team members can log into the dashboard. We're getting a 500 error.",
    "Request – Discount Inquiry": "Do you offer any discounts for non-profit organizations?",
    "Problem – Sync Failures": "Our CRM integration has been failing to sync every night for the past two weeks. Each morning we open a new ticket, but the issue persists.",
    "Change – Subscription Downgrade": "We need to downgrade our plan from Enterprise to Pro starting next billing cycle.",
}

# ============================
# MLS 3 - CASE STUDY 2: LEGAL DOCUMENT SUMMARIZATION
# ============================

LEGAL_SUMMARIZATION_V1 = """
Summarize the case details/judgements provided in the user input. Be specific and concise in your summary.
"""

LEGAL_SUMMARIZATION_V2 = """
You are a legal expert tasked with summarizing court judgments, petitions, and appeals.
Your summaries must be concise, accurate, and structured, capturing the key legal principles, facts, and outcomes while omitting redundant details.

Use the following guidelines for your summary:
1. Extract key elements: case context, legal issue, judgment with HELD section, and critical references.
2. Structure with opening line, numbered legal principles in HELD section, and retained paragraph markers.
3. Omit procedural history, lengthy citations, and redundant details.
4. Maintain formal, neutral tone in passive voice under 150 words.
"""

LEGAL_JUDGE_SYSTEM = """
You are tasked with evaluating AI-generated summaries of court judgments against the original legal documents.

### Input Format:
- ###Legal-doc: The original court judgment text
- ###Summary: The AI-generated summary to be evaluated

### Evaluation Criteria (Rate 1-5):
1 - Criteria not met
2 - Minimally met
3 - Partially met
4 - Mostly met
5 - Fully met

### Evaluation Metrics:
1. COMPLETENESS: Includes all key elements — case context, legal issue, judgment (HELD section), and references.
2. VERACITY: All facts and legal principles are correctly extracted. No unsupported claims or misinterpretations.
3. STRUCTURE: Follows required format — opening line, numbered HELD points, paragraph references.
4. TERMINOLOGICAL RIGOR: Uses exact legal terminology. Maintains neutral, formal tone. Stays under 150 words.

### Output format (respond in valid JSON only):
```json
{
  "completeness": {"score": <1-5>, "explanation": "<brief>"},
  "veracity": {"score": <1-5>, "explanation": "<brief>"},
  "structure": {"score": <1-5>, "explanation": "<brief>"},
  "terminological_rigor": {"score": <1-5>, "explanation": "<brief>"},
  "score": <average 1-5>,
  "recommendation": "APPROVE | REVISE | REJECT"
}
```
"""

LEGAL_JUDGE_USER_TEMPLATE = """
###Legal-doc
{legal_doc}

###Summary
{summary}
"""

# Reference (gold) summaries for BERTScore evaluation
SAMPLE_LEGAL_DOC_REFERENCES = {
    "Infosys Trade Mark Case": "Infosys Technologies Ltd. appealed against IPAB's order removing its INFOSYS trade mark. HELD: The Supreme Court set aside the IPAB order, finding that the appellant had established prior and continuous use of the mark since 1981. Prior registration and consistent use creates a presumption of validity that cannot be displaced without clear evidence of prior use by the opposing party.",
    "Rent Control Dispute": "A landlord sought eviction of a long-standing commercial tenant on grounds of default and personal requirement. HELD: The Supreme Court upheld the finding of default by the first appellate authority but dismissed the eviction on grounds of personal requirement, as the landlord failed to demonstrate genuine and reasonable necessity. Eviction for personal requirement requires clear and cogent evidence of bona fide need. The tenant's occupation was upheld subject to payment of arrears.",
}

SAMPLE_LEGAL_DOCS = {
    "Infosys Trade Mark Case": """
These three appeals by special leave are directed against the order dated September 9, 2004 passed by the Intellectual Property Appellate Board (IPAB) whereby it ordered the removal of appellant's mark INFOSYS from the Register of Trade Marks in respect of computer stationery, computer manuals, printed matter for computer instructional and teaching materials, computer hardware and peripherals, and machine and machine tools.

The appellant is Infosys Technologies Limited. It was incorporated and registered under the Companies Act, 1956 on July 2, 1981 in the name of Infosys Consultants Private Limited. The appellant got the trade mark INFOSYS registered in 1987 in Classes 16 and 9 in connection with computer stationery, computer manuals, printed manual for computer instruction and teaching materials, computer hardwares, computer interface, computer peripherals, electronics telex interface, and in 1988 in Class 7 in connection with machine and machine tools and motors not for land vehicles.

On April 21, 1992, the name of the company Infosys Consultants Pvt. Limited was changed to Infosys Technologies Limited. A rival company filed for cancellation of the registered mark, contending prior use. The IPAB upheld this contention and ordered removal of the mark.

HELD: The Supreme Court, after examining the evidence of use and registration, held that the appellant had established prior and continuous use of the mark INFOSYS since 1981. The IPAB order was set aside. Prior registration and consistent use of a mark creates a presumption of validity that cannot be overridden without clear evidence of prior use by the opposing party.
""",
    "Rent Control Dispute": """
This appeal arises from a dispute between a landlord and tenant under the Rent Control Act. The tenant has been in occupation of commercial premises since 1978 under a monthly tenancy at a rent of Rs. 500 per month. The landlord filed an eviction petition in 1995 on grounds of default in payment of rent and bona fide requirement of the premises for personal use.

The Rent Controller dismissed the petition, finding no genuine default and holding that the landlord's alleged requirement was not bona fide. The appellate authority reversed this finding in part, holding default proved but denying eviction on the ground of personal requirement. The High Court restored the Rent Controller's order in full.

HELD: The Supreme Court examined the concurrent findings and held that on the question of default, the findings of the first appellate authority were not perverse. However, on the question of bona fide requirement, the landlord failed to demonstrate genuine personal necessity. Eviction on the ground of personal requirement requires clear and cogent evidence of reasonable and genuine need. The appeal was dismissed; the tenant's continued occupation was upheld subject to payment of arrears.
""",
}

SAMPLE_POLICIES = {
    "refund": """Refund Policy: Full refunds available within 24 hours for damaged, 
    spoiled, or incorrect items. Missing items refunded immediately. Quality concerns 
    reviewed case-by-case. Refunds processed in 3-5 business days.""",
    
    "delivery": """Delivery Policy: Standard delivery within 2 hours. Express delivery 
    available in 45 minutes for premium members. We deliver 7 AM to 11 PM daily. 
    Delivery fee: $2.99 (free for orders over $50).""",
    
    "return": """Return Policy: Fresh produce and perishables can be reported within 
    24 hours of delivery for refund/replacement. Non-perishable items can be returned 
    within 7 days if unopened."""
}
