"""
Customer Support Automation with LLM - Streamlit App
A comprehensive demonstration of prompt engineering for customer support automation
"""

import streamlit as st
import sys
import os
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.llm_service import LLMService
from src.prompts import (
    SYSTEM_PROMPT, CATEGORIZATION_PROMPT, GENERIC_INQUIRY_PROMPT,
    REFUND_REQUEST_PROMPT, ORDER_STATUS_PROMPT, POLICY_QUERY_PROMPT,
    COMPLAINT_HANDLING_PROMPT, GUARDRAILS_PROMPT, JUDGE_EVALUATION_PROMPT,
    SAMPLE_ORDERS, SAMPLE_POLICIES
)

# Page configuration
st.set_page_config(
    page_title="FreshCart AI Support Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .category-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        background-color: #f0f8ff;
        margin: 1rem 0;
    }
    .response-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f5f5f5;
        margin: 1rem 0;
    }
    .safe-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        background-color: #e8f5e9;
    }
    .unsafe-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        background-color: #ffebee;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'llm_service' not in st.session_state:
    st.session_state.llm_service = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0

# Sidebar - API Configuration & Educational Content
with st.sidebar:
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/logo.svg", width=50)
    st.title("🛒 FreshCart AI")
    st.markdown("---")
    
    # API Key from Environment
    st.subheader("⚙️ Configuration")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        if st.session_state.llm_service is None:
            st.session_state.llm_service = LLMService(api_key=api_key)
            st.success("✅ Connected to OpenAI!")
    else:
        st.error("❌ OPENAI_API_KEY not found in environment variables")
        st.info("Set it with: $env:OPENAI_API_KEY = 'sk-...'")
    
    st.markdown("---")
    
    # Educational Content
    st.subheader("📚 Learning Objectives")
    with st.expander("🎯 Case Study Overview"):
        st.markdown("""
        **Context:** Online Food & Grocery Delivery Platform
        
        **Key Focus Areas:**
        1. Request Categorization
        2. Generic Inquiry Handling
        3. Refund Request Processing
        4. Order Status Management
        5. Policy Explanations
        6. Complaint Resolution
        7. Response Safety (Guardrails)
        8. Quality Evaluation (LLM-as-a-Judge)
        """)
    
    with st.expander("🏭 Industry Best Practices"):
        st.markdown("""
        **Real-World Considerations:**
        
        1. **Latency Matters**: Sub-2-second responses
        2. **Cost Optimization**: Use smaller models when possible
        3. **Guardrails are Critical**: Always validate outputs
        4. **Monitoring**: Track response quality continuously
        5. **Fallback Mechanisms**: Human escalation paths
        6. **Context Management**: Keep conversation history
        7. **A/B Testing**: Test prompts before deployment
        8. **Compliance**: GDPR, data privacy, PII handling
        """)
    
    with st.expander("💡 Prompt Engineering Tips"):
        st.markdown("""
        - **Be Specific**: Clear instructions → better outputs
        - **Few-Shot Learning**: Provide examples
        - **Temperature Control**: Lower for factual, higher for creative
        - **Structured Output**: Request specific formats
        - **Chain-of-Thought**: Break complex tasks into steps
        - **Iterative Refinement**: Test and improve prompts
        """)
    
    st.markdown("---")
    
    # Statistics
    if st.session_state.llm_service:
        stats = st.session_state.llm_service.get_stats()
        st.subheader("📊 Session Statistics")
        st.metric("API Calls", stats['total_calls'])
        st.metric("Total Tokens", st.session_state.total_tokens)
        st.metric("Model", stats['model'])

# Main Content
st.markdown('<div class="main-header">🛒 FreshCart AI Support Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent Customer Support Automation with LLM</div>', unsafe_allow_html=True)

# Check if API key is configured
if not api_key:
    st.error("⚠️ OPENAI_API_KEY not found in environment variables")
    st.info("""
    **Setup Required:**
    1. Set environment variable: `$env:OPENAI_API_KEY = "sk-your-key"`
    2. Or create a .env file with: `OPENAI_API_KEY=sk-your-key`
    3. Restart the app
    """)
    st.stop()

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏷️ Categorization",
    "💬 Generic Inquiry",
    "💰 Refund Request",
    "📦 Order Status",
    "📋 Policy Query",
    "😟 Complaint Handling",
    "🛡️ Guardrails",
    "⚖️ LLM-as-a-Judge"
])

# ========================================
# TAB 1: CATEGORIZATION
# ========================================
with tab1:
    st.header("🏷️ Request Categorization")
    st.markdown("""
    **Purpose:** Automatically categorize incoming support requests to route them to the right handler.
    
    **Why it matters:** In production, this is the first step. Proper categorization enables:
    - Faster routing to specialized teams
    - Priority queue management
    - SLA tracking by category
    - Better analytics and insights
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Customer Message")
        
        sample_messages = [
            "Custom message...",
            "My order hasn't arrived yet and it's been 3 hours!",
            "I received rotten tomatoes in my order. I want my money back.",
            "How do I add a new delivery address to my account?",
            "What's your policy on returning fresh produce?",
            "This is unacceptable! My groceries were left outside in the rain!"
        ]
        
        selected_sample = st.selectbox("Sample Messages:", sample_messages)
        
        if selected_sample == "Custom message...":
            customer_msg = st.text_area("Enter customer message:", height=150)
        else:
            customer_msg = st.text_area("Enter customer message:", value=selected_sample, height=150)
        
        if st.button("🔍 Categorize Request", type="primary"):
            if customer_msg:
                with st.spinner("Analyzing request..."):
                    result = st.session_state.llm_service.categorize_request(
                        customer_msg,
                        CATEGORIZATION_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("Categorization Result")
                            st.markdown(f'<div class="category-box">{result["response"]}</div>', 
                                      unsafe_allow_html=True)
                            
                            st.info(f"""
                            **Model:** {result['model']}  
                            **Tokens Used:** {result['tokens_used']}  
                            **Response Time:** {result['elapsed_time']:.2f}s
                            """)
                            
                            st.markdown("**💡 Production Insight:**")
                            st.write("""
                            In a real system, this category would trigger:
                            - Routing to specialized queues
                            - SLA timer starts
                            - Relevant context loading
                            - Priority scoring
                            """)
            else:
                st.warning("Please enter a customer message.")

# ========================================
# TAB 2: GENERIC INQUIRY
# ========================================
with tab2:
    st.header("💬 Generic Inquiry Handling")
    st.markdown("""
    **Purpose:** Handle general questions about the service, account, or platform features.
    
    **Industry Application:** These represent 40-50% of support tickets. Automation here provides:
    - 24/7 instant responses
    - Consistent information delivery
    - Reduced load on human agents
    - Multilingual support capability
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Customer Inquiry")
        
        inquiry_samples = [
            "Custom inquiry...",
            "How do I change my delivery time preference?",
            "Do you deliver to my area? My zip code is 12345.",
            "What payment methods do you accept?",
            "How do I become a premium member?"
        ]
        
        selected_inquiry = st.selectbox("Sample Inquiries:", inquiry_samples)
        
        if selected_inquiry == "Custom inquiry...":
            inquiry_msg = st.text_area("Enter inquiry:", height=100)
        else:
            inquiry_msg = st.text_area("Enter inquiry:", value=selected_inquiry, height=100)
        
        if st.button("💬 Generate Response", type="primary", key="inquiry_btn"):
            if inquiry_msg:
                with st.spinner("Generating response..."):
                    result = st.session_state.llm_service.handle_inquiry(
                        inquiry_msg,
                        GENERIC_INQUIRY_PROMPT,
                        SYSTEM_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("AI Response")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
            else:
                st.warning("Please enter an inquiry.")

# ========================================
# TAB 3: REFUND REQUEST
# ========================================
with tab3:
    st.header("💰 Refund Request Handling")
    st.markdown("""
    **Purpose:** Process refund requests with policy compliance and empathy.
    
    **Critical in Production:** Refunds involve money - mistakes are costly. This system:
    - Ensures policy compliance
    - Maintains consistent decision-making
    - Reduces disputes and chargebacks
    - Tracks refund patterns for quality improvement
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Refund Request Details")
        
        refund_samples = [
            "Custom request...",
            "Half the vegetables in my order were spoiled. I want a full refund!",
            "I'm missing 2 items from my order - the milk and bread.",
            "The delivery was 45 minutes late and my ice cream melted."
        ]
        
        selected_refund = st.selectbox("Sample Requests:", refund_samples)
        
        if selected_refund == "Custom request...":
            refund_msg = st.text_area("Customer message:", height=100)
        else:
            refund_msg = st.text_area("Customer message:", value=selected_refund, height=100)
        
        order_id = st.selectbox("Order ID:", list(SAMPLE_ORDERS.keys()))
        order_details = SAMPLE_ORDERS[order_id]
        
        st.json(order_details)
        
        if st.button("💰 Process Refund Request", type="primary", key="refund_btn"):
            if refund_msg:
                with st.spinner("Processing refund request..."):
                    result = st.session_state.llm_service.handle_refund(
                        refund_msg,
                        str(order_details),
                        REFUND_REQUEST_PROMPT,
                        SYSTEM_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("AI Response")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
                            
                            st.markdown("**💡 Production Consideration:**")
                            st.write("""
                            In production, this would:
                            - Trigger automated refund in payment system
                            - Send confirmation email
                            - Log for fraud detection
                            - Update customer satisfaction scores
                            """)
            else:
                st.warning("Please enter a refund request.")

# ========================================
# TAB 4: ORDER STATUS
# ========================================
with tab4:
    st.header("📦 Order Status Queries")
    st.markdown("""
    **Purpose:** Provide real-time order updates and manage delivery expectations.
    
    **Value in Production:** Order tracking queries are high-volume, low-complexity:
    - Perfect for automation (95%+ accuracy possible)
    - Reduces "where is my order?" calls dramatically
    - Proactive communication reduces anxiety
    - Integration with logistics systems for real-time data
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Order Status Query")
        
        status_samples = [
            "Custom query...",
            "Where is my order? It's been 2 hours!",
            "When will my order arrive? Order ID: ORD456",
            "My order status shows 'Delayed'. What does that mean?"
        ]
        
        selected_status = st.selectbox("Sample Queries:", status_samples)
        
        if selected_status == "Custom query...":
            status_msg = st.text_area("Customer query:", height=100)
        else:
            status_msg = st.text_area("Customer query:", value=selected_status, height=100)
        
        order_id_status = st.selectbox("Order ID:", list(SAMPLE_ORDERS.keys()), key="status_order")
        order_info = SAMPLE_ORDERS[order_id_status]
        
        st.json(order_info)
        
        if st.button("📦 Check Order Status", type="primary", key="status_btn"):
            if status_msg:
                with st.spinner("Checking order status..."):
                    result = st.session_state.llm_service.handle_order_status(
                        status_msg,
                        str(order_info),
                        ORDER_STATUS_PROMPT,
                        SYSTEM_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("AI Response")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
            else:
                st.warning("Please enter a query.")

# ========================================
# TAB 5: POLICY QUERY
# ========================================
with tab5:
    st.header("📋 Policy-Related Queries")
    st.markdown("""
    **Purpose:** Explain company policies clearly and consistently.
    
    **Why LLMs Excel Here:**
    - Can explain complex policies in simple terms
    - Adapts explanation to user's question
    - Maintains consistency across all agents
    - Reduces misunderstandings and disputes
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Policy Question")
        
        policy_samples = [
            "Custom question...",
            "What's your refund policy if I receive damaged items?",
            "How does your delivery guarantee work?",
            "Can I return fresh produce if I don't like the quality?"
        ]
        
        selected_policy_q = st.selectbox("Sample Questions:", policy_samples)
        
        if selected_policy_q == "Custom question...":
            policy_msg = st.text_area("Customer question:", height=100)
        else:
            policy_msg = st.text_area("Customer question:", value=selected_policy_q, height=100)
        
        policy_type = st.selectbox("Related Policy:", list(SAMPLE_POLICIES.keys()))
        policy_context = SAMPLE_POLICIES[policy_type]
        
        st.text_area("Policy Context:", value=policy_context, height=100, disabled=True)
        
        if st.button("📋 Explain Policy", type="primary", key="policy_btn"):
            if policy_msg:
                with st.spinner("Generating explanation..."):
                    result = st.session_state.llm_service.handle_policy(
                        policy_msg,
                        policy_context,
                        POLICY_QUERY_PROMPT,
                        SYSTEM_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("AI Response")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
            else:
                st.warning("Please enter a question.")

# ========================================
# TAB 6: COMPLAINT HANDLING
# ========================================
with tab6:
    st.header("😟 Complaint Handling")
    st.markdown("""
    **Purpose:** De-escalate complaints with empathy and concrete solutions.
    
    **Critical Success Factors:**
    - Acknowledge feelings first (empathy)
    - Take responsibility (no defensiveness)
    - Provide specific solutions
    - Prevent escalation to social media/reviews
    
    **Industry Stat:** A well-handled complaint increases loyalty more than if the problem never occurred!
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Customer Complaint")
        
        complaint_samples = [
            "Custom complaint...",
            "This is the third time my order has been wrong! Your service is terrible!",
            "I'm extremely disappointed. The driver left my groceries outside without ringing the bell.",
            "Your app keeps crashing and I missed my delivery window because of it!"
        ]
        
        selected_complaint = st.selectbox("Sample Complaints:", complaint_samples)
        
        if selected_complaint == "Custom complaint...":
            complaint_msg = st.text_area("Customer complaint:", height=100)
        else:
            complaint_msg = st.text_area("Customer complaint:", value=selected_complaint, height=100)
        
        issue_type = st.selectbox(
            "Issue Type:",
            ["Quality Issue", "Delivery Problem", "App/Technical Issue", "Customer Service Issue", "Repeat Problem"]
        )
        
        if st.button("😟 Handle Complaint", type="primary", key="complaint_btn"):
            if complaint_msg:
                with st.spinner("Crafting empathetic response..."):
                    result = st.session_state.llm_service.handle_complaint(
                        complaint_msg,
                        issue_type,
                        COMPLAINT_HANDLING_PROMPT,
                        SYSTEM_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("AI Response")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
                            
                            st.markdown("**💡 What Makes This Work:**")
                            st.write("""
                            - **Acknowledges emotion** ("I understand your frustration")
                            - **Takes responsibility** (no excuses)
                            - **Specific solution** (not vague promises)
                            - **Compensation** (when appropriate)
                            - **Prevention assurance** (we're fixing this)
                            """)
            else:
                st.warning("Please enter a complaint.")

# ========================================
# TAB 7: GUARDRAILS
# ========================================
with tab7:
    st.header("🛡️ Guardrails - Safety & Compliance")
    st.markdown("""
    **Purpose:** Ensure all AI responses are safe, compliant, and appropriate before showing to customers.
    
    **Critical in Production:** NEVER send LLM output directly to customers without validation!
    
    **What We Check:**
    1. **Toxic Language**: Rude, offensive, or unprofessional content
    2. **PII Exposure**: Accidental disclosure of personal information
    3. **Policy Violations**: Promises outside company policy
    4. **Discriminatory Content**: Biased or discriminatory language
    5. **Unsafe Advice**: Harmful recommendations
    
    **Real-World Impact:** One unfiltered bad response can damage brand reputation and cause legal issues.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Response to Check")
        
        test_responses = [
            "Custom response...",
            "I understand your frustration. I've processed a full refund of $24.99 to your account. You should see it in 3-5 business days.",
            "Look, you're being unreasonable. We have thousands of customers and can't cater to everyone's demands.",
            "I've refunded you $100 even though our policy doesn't cover this. Don't tell anyone!",
            "I can see your credit card ending in 4532 was charged. Your address at 123 Main St, email john@email.com is confirmed."
        ]
        
        selected_test = st.selectbox("Test Responses:", test_responses)
        
        if selected_test == "Custom response...":
            test_response = st.text_area("Enter response to check:", height=150)
        else:
            test_response = st.text_area("Enter response to check:", value=selected_test, height=150)
        
        if st.button("🛡️ Run Guardrails Check", type="primary", key="guard_btn"):
            if test_response:
                with st.spinner("Running safety checks..."):
                    result = st.session_state.llm_service.check_guardrails(
                        test_response,
                        GUARDRAILS_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("Guardrails Analysis")
                            
                            # Parse the response to determine if safe
                            response_text = result["response"]
                            is_safe = "SAFE: YES" in response_text.upper()
                            
                            if is_safe:
                                st.markdown(
                                    f'<div class="safe-box">✅ <strong>SAFE TO SEND</strong></div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(
                                    f'<div class="unsafe-box">⛔ <strong>UNSAFE - DO NOT SEND</strong></div>',
                                    unsafe_allow_html=True
                                )
                            
                            st.markdown(f'<div class="response-box">{response_text}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
                            
                            st.markdown("**🏭 Production Implementation:**")
                            st.code("""
# Pseudo-code for production guardrails
def send_response_to_customer(ai_response):
    # Step 1: Run guardrails check
    safety_check = check_guardrails(ai_response)
    
    if not safety_check.is_safe:
        # Log the incident
        log_unsafe_response(ai_response, safety_check.issues)
        
        # Route to human agent
        escalate_to_human(customer_id)
        
        # Send fallback message
        return "I'm connecting you with a specialist..."
    
    # Step 2: Send safe response
    send_to_customer(ai_response)
                            """, language="python")
            else:
                st.warning("Please enter a response to check.")

# ========================================
# TAB 8: LLM-AS-A-JUDGE
# ========================================
with tab8:
    st.header("⚖️ LLM-as-a-Judge - Quality Evaluation")
    st.markdown("""
    **Purpose:** Use an LLM to evaluate the quality of another LLM's responses.
    
    **Why This Matters in Production:**
    
    1. **Continuous Monitoring**: Evaluate 100% of responses automatically
    2. **A/B Testing**: Compare different prompts systematically
    3. **Training Data**: Identify good/bad examples for fine-tuning
    4. **Quality Metrics**: Track improvement over time
    5. **Cost-Effective**: Much cheaper than human evaluation at scale
    
    **Industry Application:** Companies like Anthropic, OpenAI use this technique extensively
    to improve their models and prompts.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Response to Evaluate")
        
        st.text_area("Customer Request:", value="My order arrived 2 hours late and the ice cream melted!", height=80, disabled=True, key="judge_req")
        
        eval_responses = [
            "Custom response...",
            "I sincerely apologize for the delayed delivery and the impact on your ice cream. I've issued a full refund for the ice cream ($8.99) and added a 20% discount code (SORRY20) to your account for your next order. We're also reporting this to our logistics team to prevent future delays in your area. Is there anything else I can help you with?",
            "We're sorry about that. Here's a refund.",
            "Delays happen sometimes due to traffic. The ice cream is non-refundable as per our policy. Thank you for understanding."
        ]
        
        selected_eval = st.selectbox("Responses to Evaluate:", eval_responses)
        
        if selected_eval == "Custom response...":
            eval_response = st.text_area("AI response to evaluate:", height=150)
        else:
            eval_response = st.text_area("AI response to evaluate:", value=selected_eval, height=150)
        
        if st.button("⚖️ Evaluate Response", type="primary", key="judge_btn"):
            if eval_response:
                with st.spinner("Evaluating response quality..."):
                    result = st.session_state.llm_service.evaluate_response(
                        "My order arrived 2 hours late and the ice cream melted!",
                        eval_response,
                        JUDGE_EVALUATION_PROMPT
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens += result['tokens_used']
                        
                        with col2:
                            st.subheader("Quality Evaluation")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
                            
                            st.markdown("**💡 Using This in Production:**")
                            st.code("""
# Production monitoring pipeline
def evaluate_and_log_response(customer_msg, ai_response):
    # Get evaluation
    evaluation = llm_judge.evaluate(customer_msg, ai_response)
    
    # Log to database
    db.log_response(
        message=customer_msg,
        response=ai_response,
        scores=evaluation.scores,
        recommendation=evaluation.recommendation
    )
    
    # Alert if quality drops
    if evaluation.overall_score < 3.0:
        alert_team("Low quality response detected")
    
    # Use for A/B testing
    ab_test.record_variant_score(
        variant="prompt_v2",
        score=evaluation.overall_score
    )
                            """, language="python")
                            
                            st.markdown("**📊 What To Track:**")
                            st.write("""
                            - Average scores per category over time
                            - Distribution of APPROVE/REVISE/REJECT
                            - Correlation with customer satisfaction
                            - Prompt version performance comparison
                            """)
            else:
                st.warning("Please enter a response to evaluate.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <strong>🛒 FreshCart AI Support Assistant</strong><br>
    Built with Streamlit • Powered by OpenAI GPT-4<br>
    <em>A demonstration of production-grade LLM applications for customer support automation</em>
</div>
""", unsafe_allow_html=True)
