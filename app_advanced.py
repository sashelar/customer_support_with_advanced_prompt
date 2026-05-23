"""
Advanced Prompt Engineering Demo - Week 2 Techniques
Demonstrates: Few-Shot, Chain-of-Thought, Rephrase & Respond, Self-Consistency, LLM-as-a-Judge
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.llm_service_enhanced import EnhancedLLMService
from src.prompts_enhanced import *

# Page configuration
st.set_page_config(
    page_title="Advanced Prompt Engineering - Week 2",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .technique-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
        background-color: #FFF5F5;
        margin: 1rem 0;
    }
    .comparison-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #F0F8FF;
        margin: 0.5rem 0;
    }
    .json-output {
        background-color: #2D2D2D;
        color: #F8F8F2;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'enhanced_llm_service' not in st.session_state:
    st.session_state.enhanced_llm_service = None
if 'total_tokens_advanced' not in st.session_state:
    st.session_state.total_tokens_advanced = 0

# Sidebar
with st.sidebar:
    st.title("🧠 Advanced Techniques")
    st.markdown("### Week 2: Prompt Engineering")
    st.markdown("---")
    
    # API Key from Environment
    st.subheader("⚙️ Configuration")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        if st.session_state.enhanced_llm_service is None:
            st.session_state.enhanced_llm_service = EnhancedLLMService(api_key=api_key)
            st.success("✅ Connected to OpenAI!")
    else:
        st.error("❌ OPENAI_API_KEY not found")
        st.info("Set: $env:OPENAI_API_KEY = 'sk-...'")
    
    st.markdown("---")
    
    # Learning Objectives
    st.subheader("📚 Learning Objectives")
    with st.expander("Week 2 Techniques"):
        st.markdown("""
        1. **Few-Shot Learning**
           - Show examples, not just instructions
           - Format specification
           
        2. **Chain-of-Thought (CoT)**
           - Step-by-step reasoning
           - Explainable outputs
           
        3. **Two-Stage CoT**
           - Break complex tasks
           - Analysis → Recommendations
           
        4. **Self-Consistency**
           - Generate multiple answers
           - Select most consistent
           
        5. **Rephrase & Respond**
           - Clarify ambiguous questions
           - Better understanding
           
        6. **LLM-as-a-Judge**
           - Automated evaluation
           - Multi-dimensional scoring
        """)
    
    st.markdown("---")
    
    # Statistics
    if st.session_state.enhanced_llm_service:
        stats = st.session_state.enhanced_llm_service.get_stats()
        st.subheader("📊 Session Stats")
        st.metric("API Calls", stats['total_calls'])
        st.metric("Total Tokens", st.session_state.total_tokens_advanced)
        st.metric("Model", stats['model'])

# Main Content
st.markdown("# 🧠 Advanced Prompt Engineering Techniques")
st.markdown("### Based on Week 2: Prompt Engineering Fundamentals")

# Check API key
if not api_key:
    st.error("⚠️ OPENAI_API_KEY not found in environment")
    st.info("Set it with: `$env:OPENAI_API_KEY = 'sk-your-key'`")
    st.stop()

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Few-Shot Learning",
    "🧵 Chain-of-Thought",
    "🔄 Two-Stage CoT",
    "✅ Self-Consistency",
    "📝 Rephrase & Respond",
    "⚖️ LLM-as-a-Judge"
])

# ========================================
# TAB 1: FEW-SHOT LEARNING
# ========================================
with tab1:
    st.header("🎯 Few-Shot Learning")
    st.markdown("""
    **Concept:** Show the model examples of input-output pairs to specify the expected format.
    
    **Key Insight:** The model doesn't "learn" from example content - it learns the *format*.
    This is why we can even swap labels in examples and still get correct outputs!
    
    **Use Case:** When you need consistent structured output (JSON, specific formats)
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        
        approach = st.radio(
            "Select Approach:",
            ["Few-Shot (with examples)", "Zero-Shot (no examples)"],
            help="Compare few-shot vs zero-shot"
        )
        
        sample_messages = [
            "Custom message...",
            "This is the third time my order has been wrong!",
            "I received spoiled milk. I want a refund.",
            "How do I change my delivery address?",
            "What's your policy on returns?"
        ]
        
        selected_msg = st.selectbox("Sample Messages:", sample_messages)
        
        if selected_msg == "Custom message...":
            customer_msg = st.text_area("Enter message:", height=100)
        else:
            customer_msg = st.text_area("Enter message:", value=selected_msg, height=100)
        
        # Show what will be sent to API
        with st.expander("📋 Click to view prompt structure"):
            if approach == "Few-Shot (with examples)":
                prompt_messages = [{"role": "developer", "content": FEW_SHOT_CATEGORIZATION_SYSTEM}]
                prompt_messages.extend(FEW_SHOT_CATEGORIZATION_EXAMPLES)
                prompt_messages.append({"role": "user", "content": customer_msg if customer_msg else "<your message here>"})
            else:
                prompt_messages = [
                    {"role": "developer", "content": FEW_SHOT_CATEGORIZATION_SYSTEM},
                    {"role": "user", "content": customer_msg if customer_msg else "<your message here>"}
                ]
            
            st.json(prompt_messages)
            st.caption(f"Total messages in prompt: {len(prompt_messages)}")
        
        if st.button("🎯 Categorize", type="primary", key="fewshot_btn"):
            if customer_msg:
                with st.spinner("Categorizing..."):
                    if approach == "Few-Shot (with examples)":
                        result = st.session_state.enhanced_llm_service.few_shot_categorize(
                            customer_msg,
                            FEW_SHOT_CATEGORIZATION_SYSTEM,
                            FEW_SHOT_CATEGORIZATION_EXAMPLES
                        )
                    else:
                        result = st.session_state.enhanced_llm_service.zero_shot_categorize(
                            customer_msg,
                            FEW_SHOT_CATEGORIZATION_SYSTEM
                        )
                    
                    if result['success']:
                        st.session_state.total_tokens_advanced += result['tokens_used']
                        
                        with col2:
                            st.subheader("Result")
                            st.markdown(f'<div class="technique-card">{result["response"]}</div>', 
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
                            
                            st.markdown("**💡 Key Takeaway:**")
                            if approach == "Few-Shot (with examples)":
                                st.write("""
                                Few-shot prompting provides 3 examples showing the exact JSON format expected.
                                The model learns the structure, not the content!
                                """)
                            else:
                                st.write("""
                                Zero-shot relies only on instructions in the system message.
                                May be less consistent with complex output formats.
                                """)
            else:
                st.warning("Please enter a message")

# ========================================
# TAB 2: CHAIN-OF-THOUGHT
# ========================================
with tab2:
    st.header("🧵 Chain-of-Thought (CoT)")
    st.markdown("""
    **Concept:** Ask the model to explain its reasoning step-by-step before giving the final answer.
    
    **Why it works:** Breaking down complex tasks into steps improves accuracy and makes outputs explainable.
    
    **Key phrase:** "Take a step-by-step approach" or "Explain your reasoning"
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Customer Complaint")
        
        cot_samples = [
            "Custom complaint...",
            "My order #12345 arrived 2 hours late. The ice cream melted ($15), and 3 items were missing (milk $5, bread $4, eggs $6). I had to order from another store which cost me $20 delivery. I explicitly need a refund!",
            "Received order ORD789. Half the vegetables are rotten. Spent $45 total, wasted $22 on bad produce. Want my money back ASAP!",
        ]
        
        selected_complaint = st.selectbox("Sample Complaints:", cot_samples)
        
        if selected_complaint == "Custom complaint...":
            complaint = st.text_area("Enter complaint:", height=150)
        else:
            complaint = st.text_area("Enter complaint:", value=selected_complaint, height=150)
        
        # Show what will be sent to API
        with st.expander("📋 Click to view prompt structure"):
            prompt_messages = [
                {"role": "developer", "content": ENTITY_EXTRACTION_COT_SYSTEM},
                {"role": "user", "content": complaint if complaint else "<your complaint here>"}
            ]
            st.json(prompt_messages)
            st.caption(f"Total messages: {len(prompt_messages)} | Note: CoT asks for step-by-step reasoning in system message")
        
        if st.button("🧵 Analyze with CoT", type="primary", key="cot_btn"):
            if complaint:
                with st.spinner("Analyzing step-by-step..."):
                    result = st.session_state.enhanced_llm_service.cot_entity_extraction(
                        complaint,
                        ENTITY_EXTRACTION_COT_SYSTEM
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens_advanced += result['tokens_used']
                        
                        with col2:
                            st.subheader("Analysis")
                            st.markdown(f'<div class="technique-card">{result["response"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']} | Time: {result['elapsed_time']:.2f}s")
                            
                            st.markdown("**💡 What Happened:**")
                            st.write("""
                            The model:
                            1. Broke down the task into steps
                            2. Explained its reasoning for each extraction
                            3. Provided the final structured JSON
                            
                            This makes the output explainable and verifiable!
                            """)
            else:
                st.warning("Please enter a complaint")

# ========================================
# TAB 3: TWO-STAGE CoT
# ========================================
with tab3:
    st.header("🔄 Two-Stage Chain-of-Thought")
    st.markdown("""
    **Concept:** Break complex tasks into two stages:
    1. **Stage 1:** Analyze the input (extract information, identify themes)
    2. **Stage 2:** Generate recommendations based on Stage 1 output
    
    **Why it's powerful:** Each stage focuses on one clear task, improving quality.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Customer Feedback")
        
        feedback = st.text_area(
            "Enter feedback:",
            value="The delivery was 2 hours late. Driver didn't call. Ice cream melted, vegetables wilted. Spent $60, half was wasted. Customer service was unhelpful. This is my third bad experience. Considering switching to competitors.",
            height=150
        )
        
        # Show what will be sent to API
        with st.expander("📋 Click to view Stage 1 prompt"):
            stage1_messages = [
                {"role": "developer", "content": COT_STAGE1_ANALYSIS_SYSTEM},
                {"role": "user", "content": feedback}
            ]
            st.json(stage1_messages)
            st.caption("Stage 1: Analysis phase")
        
        with st.expander("📋 Stage 2 prompt (generated after Stage 1)"):
            st.info("Stage 2 prompt will include the output from Stage 1 as context")
            st.code("""
# Example Stage 2 structure:
{
  "role": "developer",
  "content": "Generate recommendations system message..."
},
{
  "role": "user", 
  "content": "Analysis from Stage 1: <stage1_output>"
}
            """)
        
        if st.button("🔄 Two-Stage Analysis", type="primary", key="twostage_btn"):
            if feedback:
                with st.spinner("Stage 1: Analyzing feedback..."):
                    result = st.session_state.enhanced_llm_service.two_stage_cot(
                        feedback,
                        COT_STAGE1_ANALYSIS_SYSTEM,
                        COT_STAGE2_RECOMMENDATIONS_SYSTEM
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens_advanced += result['total_tokens']
                        
                        with col2:
                            st.subheader("Results")
                            
                            st.markdown("**Stage 1: Analysis**")
                            st.markdown(f'<div class="comparison-box">{result["stage1_analysis"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.markdown("**Stage 2: Recommendations**")
                            st.markdown(f'<div class="comparison-box">{result["stage2_recommendations"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Total Tokens: {result['total_tokens']} | Total Time: {result['total_time']:.2f}s")
                            
                            st.markdown("**💡 Benefits:**")
                            st.write("""
                            - Stage 1 focuses purely on understanding
                            - Stage 2 uses that understanding for actionable insights
                            - Each stage is simpler than doing both at once
                            - Better quality overall
                            """)
            else:
                st.warning("Please enter feedback")

# ========================================
# TAB 4: SELF-CONSISTENCY
# ========================================
with tab4:
    st.header("✅ Self-Consistency")
    st.markdown("""
    **Concept:** Generate multiple answers to the same question, then select the most consistent one.
    
    **Why it works:** For factual questions, the correct answer often appears most frequently across multiple attempts.
    
    **Use Case:** Important factual queries where accuracy is critical.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Factual Question")
        
        question = st.text_area(
            "Enter question:",
            value="What was FreshCart's total revenue increase in 2023?",
            height=100
        )
        
        num_gen = st.slider("Number of generations:", 2, 5, 3)
        
        # Show what will be sent to API
        with st.expander("📋 Click to view Generation prompt (Stage 1)"):
            gen_system = SELF_CONSISTENCY_GENERATION_SYSTEM.format(context=FRESHCART_CONTEXT)
            gen_messages = [
                {"role": "developer", "content": gen_system},
                {"role": "user", "content": question if question else "<your question>"}
            ]
            st.json(gen_messages)
            st.caption(f"This will be sent {num_gen} times with temperature=0.7 for diversity")
        
        with st.expander("📋 Click to view Selection prompt (Stage 2)"):
            st.info("After generating multiple answers, this prompt selects the best one")
            st.code("""
# Selection prompt structure:
{
  "role": "developer",
  "content": "Choose the most accurate answer..."
},
{
  "role": "user",
  "content": "Question: <question>\\n\\nGenerated Answers:\\n1. ...\\n2. ...\\n3. ..."
}
            """)
        
        if st.button("✅ Generate & Select", type="primary", key="consistency_btn"):
            if question:
                with st.spinner(f"Generating {num_gen} answers..."):
                    result = st.session_state.enhanced_llm_service.self_consistency(
                        question,
                        FRESHCART_CONTEXT,
                        SELF_CONSISTENCY_GENERATION_SYSTEM,
                        SELF_CONSISTENCY_SELECTION_SYSTEM,
                        num_generations=num_gen
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens_advanced += result['total_tokens']
                        
                        with col2:
                            st.subheader("Results")
                            
                            st.markdown(f"**Generated {num_gen} Answers:**")
                            for i, ans in enumerate(result['generated_answers'], 1):
                                st.markdown(f'<div class="comparison-box"><strong>Answer {i}:</strong><br>{ans}</div>',
                                          unsafe_allow_html=True)
                            
                            st.markdown("**Final Selected Answer:**")
                            st.markdown(f'<div class="technique-card">{result["selected_answer"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Total Tokens: {result['total_tokens']}")
                            
                            st.markdown("**💡 How it Works:**")
                            st.write("""
                            1. Generate multiple diverse answers (temp=0.7)
                            2. Analyze for consistency and accuracy
                            3. Select the most reliable answer (temp=0)
                            
                            This reduces hallucinations for factual queries!
                            """)
            else:
                st.warning("Please enter a question")

# ========================================
# TAB 5: REPHRASE & RESPOND
# ========================================
with tab5:
    st.header("📝 Rephrase & Respond")
    st.markdown("""
    **Concept:** First rephrase an ambiguous question for clarity, then answer the original question.
    
    **Why it works:** Rephrasing helps the model better understand user intent, especially for vague queries.
    
    **Two Stages:**
    1. Rephrase the question (clarify and expand)
    2. Use rephrased version to answer the original
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Customer Question")
        
        rephrase_samples = [
            "Custom question...",
            "What happened with my stuff?",
            "Why did this take so long?",
            "Can I get that back?"
        ]
        
        selected_q = st.selectbox("Sample Questions (Ambiguous):", rephrase_samples)
        
        if selected_q == "Custom question...":
            question = st.text_area("Enter question:", height=100)
        else:
            question = st.text_area("Enter question:", value=selected_q, height=100)
        
        # Show what will be sent to API
        with st.expander("📋 Click to view Rephrase prompt (Stage 1)"):
            rephrase_system = REPHRASE_SYSTEM_MESSAGE.format(context=FRESHCART_CONTEXT)
            rephrase_messages = [
                {"role": "developer", "content": rephrase_system},
                {"role": "user", "content": question if question else "<your question>"}
            ]
            st.json(rephrase_messages)
            st.caption("Stage 1: Clarify the question")
        
        with st.expander("📋 Click to view Respond prompt (Stage 2)"):
            st.info("After rephrasing, this prompt uses the clarified version to answer")
            st.code("""
# Response prompt structure:
{
  "role": "developer",
  "content": "Answer using context..."
},
{
  "role": "user",
  "content": "Original: <question>\\n\\nRephrased: <rephrased_question>"
}
            """)
        
        if st.button("📝 Rephrase & Respond", type="primary", key="rephrase_btn"):
            if question:
                with st.spinner("Step 1: Rephrasing question..."):
                    result = st.session_state.enhanced_llm_service.rephrase_and_respond(
                        question,
                        FRESHCART_CONTEXT,
                        REPHRASE_SYSTEM_MESSAGE,
                        RESPOND_SYSTEM_MESSAGE
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens_advanced += result['total_tokens']
                        
                        with col2:
                            st.subheader("Results")
                            
                            st.markdown("**Original Question:**")
                            st.markdown(f'<div class="comparison-box">{result["original_question"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.markdown("**Rephrased Question:**")
                            st.markdown(f'<div class="comparison-box">{result["rephrased_question"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.markdown("**Final Answer:**")
                            st.markdown(f'<div class="technique-card">{result["final_answer"]}</div>',
                                      unsafe_allow_html=True)
                            
                            st.info(f"Total Tokens: {result['total_tokens']}")
                            
                            st.markdown("**💡 Benefits:**")
                            st.write("""
                            - Clarifies vague questions
                            - Better understanding of user intent
                            - More accurate and relevant answers
                            - Helps with ambiguous pronouns ("this", "that", "it")
                            """)
            else:
                st.warning("Please enter a question")

# ========================================
# TAB 6: LLM-AS-A-JUDGE
# ========================================
with tab6:
    st.header("⚖️ LLM-as-a-Judge (Enhanced)")
    st.markdown("""
    **Concept:** Use an LLM to evaluate another LLM's output across multiple dimensions.
    
    **Why it's powerful:**
    - Evaluate 100% of responses automatically
    - Multi-dimensional scoring (not just pass/fail)
    - Scalable quality monitoring
    - A/B testing different prompts
    
    **Evaluation Dimensions:** Faithfulness, Relevance, Completeness, Empathy, Policy Compliance, Actionability
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Response to Evaluate")
        
        st.text_area(
            "Customer Request:",
            value="My order arrived 3 hours late and the ice cream melted. I want a refund!",
            height=80,
            disabled=True
        )
        
        response_samples = [
            "Custom response...",
            "I sincerely apologize for the delayed delivery and the melted ice cream. I've processed a full refund of $8.99 for the ice cream and added a 20% discount code (SORRY20) to your account for your next order. The refund will appear in 3-5 business days. We're also escalating this to our logistics team to prevent future delays in your area.",
            "Sorry about that. Here's a refund.",
            "Delays happen due to traffic. Ice cream is perishable so no refund available."
        ]
        
        selected_resp = st.selectbox("Responses to Evaluate:", response_samples)
        
        if selected_resp == "Custom response...":
            response_text = st.text_area("AI Response:", height=150)
        else:
            response_text = st.text_area("AI Response:", value=selected_resp, height=150)
        
        # Show what will be sent to API
        with st.expander("📋 Click to view Judge prompt"):
            judge_input = f"""###Request
My order arrived 3 hours late and the ice cream melted. I want a refund!

###Response
{response_text if response_text else "<AI response to evaluate>"}"""
            
            judge_messages = [
                {"role": "developer", "content": LLM_JUDGE_COMPREHENSIVE_SYSTEM},
                {"role": "user", "content": judge_input}
            ]
            st.json(judge_messages)
            st.caption("The judge evaluates across 6 dimensions with detailed rubrics")
        
        if st.button("⚖️ Comprehensive Evaluation", type="primary", key="judge_btn"):
            if response_text:
                with st.spinner("Evaluating across 6 dimensions..."):
                    result = st.session_state.enhanced_llm_service.comprehensive_judge(
                        "My order arrived 3 hours late and the ice cream melted. I want a refund!",
                        response_text,
                        LLM_JUDGE_COMPREHENSIVE_SYSTEM
                    )
                    
                    if result['success']:
                        st.session_state.total_tokens_advanced += result['tokens_used']
                        
                        with col2:
                            st.subheader("Evaluation Results")
                            
                            if result.get('parsed', False):
                                eval_data = result['evaluation']
                                
                                # Display metrics
                                metrics = ['faithfulness', 'relevance', 'completeness', 
                                          'empathy', 'policy_compliance', 'actionability']
                                
                                for metric in metrics:
                                    if metric in eval_data:
                                        score = eval_data[metric]['score']
                                        explanation = eval_data[metric]['explanation']
                                        
                                        st.markdown(f"**{metric.replace('_', ' ').title()}:** {score}/5")
                                        st.caption(explanation)
                                        st.progress(score / 5)
                                
                                st.markdown("---")
                                
                                # Overall
                                overall = eval_data.get('overall_score', 0)
                                recommendation = eval_data.get('recommendation', 'UNKNOWN')
                                
                                st.metric("Overall Score", f"{overall:.1f}/5.0")
                                
                                if recommendation == "APPROVE":
                                    st.success(f"✅ Recommendation: {recommendation}")
                                elif recommendation == "REVISE":
                                    st.warning(f"⚠️ Recommendation: {recommendation}")
                                else:
                                    st.error(f"❌ Recommendation: {recommendation}")
                                
                                # Strengths and improvements
                                if 'key_strengths' in eval_data:
                                    st.markdown("**Key Strengths:**")
                                    for strength in eval_data['key_strengths']:
                                        st.markdown(f"- {strength}")
                                
                                if 'areas_for_improvement' in eval_data:
                                    st.markdown("**Areas for Improvement:**")
                                    for area in eval_data['areas_for_improvement']:
                                        st.markdown(f"- {area}")
                            else:
                                st.markdown(f'<div class="technique-card">{result["response"]}</div>',
                                          unsafe_allow_html=True)
                            
                            st.info(f"Tokens: {result['tokens_used']}")
                            
                            st.markdown("**💡 Production Usage:**")
                            st.write("""
                            - Evaluate every response before sending
                            - Track quality metrics over time
                            - A/B test different prompts
                            - Identify training examples for fine-tuning
                            - Alert when quality drops below threshold
                            """)
            else:
                st.warning("Please enter a response to evaluate")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <strong>🧠 Advanced Prompt Engineering - Week 2</strong><br>
    Techniques: Few-Shot • Chain-of-Thought • Self-Consistency • Rephrase & Respond • LLM-as-a-Judge<br>
    <em>Production-ready implementations for enterprise AI applications</em>
</div>
""", unsafe_allow_html=True)
