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
