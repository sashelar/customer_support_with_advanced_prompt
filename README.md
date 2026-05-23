# 🛒 FreshCart AI Customer Support Automation

A comprehensive demonstration of **LLM-powered customer support automation** using prompt engineering, built with Python, Streamlit, and OpenAI GPT models.

## 📋 Project Overview

This application demonstrates production-grade techniques for automating customer support in an online food & grocery delivery platform. It showcases:

- **Request Categorization**: Automatically classify incoming support tickets
- **Specialized Handlers**: Different prompts for refunds, orders, policies, complaints
- **Guardrails**: Safety and compliance checking before sending responses
- **LLM-as-a-Judge**: Quality evaluation and monitoring system

## 🎯 Learning Objectives

This case study teaches:

1. **Prompt Engineering Techniques**
   - System prompts and context setting
   - Few-shot learning patterns
   - Temperature and parameter tuning
   - Structured output formatting

2. **Production Considerations**
   - Response latency optimization
   - Cost management (token usage)
   - Safety guardrails implementation
   - Quality monitoring systems
   - Error handling and fallbacks

3. **Real-World Applications**
   - Multi-turn conversations
   - Context management
   - Policy compliance
   - Customer satisfaction optimization

## 🏗️ Project Structure

```
customer_support_ai/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
├── src/
│   ├── llm_service.py     # OpenAI API integration
│   └── prompts.py         # All prompt templates
├── config/                # Configuration files
├── data/                  # Sample data
└── tests/                 # Unit tests
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or download this project**

2. **Navigate to the project directory**
   ```bash
   cd customer_support_ai
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key** (Optional - you can also enter it in the app)
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Enter your OpenAI API key in the sidebar
   - Start exploring the different use cases!

## 🎓 How to Use This Application

### For Learning & Teaching

1. **Start with Categorization Tab**
   - Understand how to route different types of requests
   - See how specific prompts improve accuracy

2. **Explore Each Handler**
   - Test different customer scenarios
   - Observe how prompts are tailored for each use case
   - Note the difference in temperature settings

3. **Test Guardrails**
   - See how safety checks prevent harmful outputs
   - Understand what can go wrong without validation

4. **Use LLM-as-a-Judge**
   - Learn how to evaluate response quality
   - Understand metrics that matter in production

### For Demonstration (10-15 minutes)

**Suggested Flow:**

1. **Introduction (2 min)**
   - Show the app interface
   - Explain the FreshCart scenario

2. **Categorization (2 min)**
   - Demo 2-3 different request types
   - Explain why categorization is the first step

3. **Specialized Handlers (4 min)**
   - Show refund handling with policy compliance
   - Show complaint handling with empathy
   - Highlight prompt engineering techniques

4. **Guardrails (3 min)**
   - Demo unsafe responses being caught
   - Explain production necessity

5. **LLM-as-a-Judge (2 min)**
   - Show quality evaluation
   - Explain monitoring strategy

6. **Q&A and Production Insights (2 min)**
   - Share real-world experiences
   - Discuss challenges and solutions

## 🏭 Industry Best Practices Demonstrated

### 1. **Prompt Engineering**
- Clear, specific instructions
- Role-based system prompts
- Structured output formats
- Temperature control by use case
- Context injection (order details, policies)

### 2. **Safety & Compliance**
- Output validation before sending
- PII detection and removal
- Policy compliance checking
- Toxic content filtering
- Human escalation paths

### 3. **Quality Assurance**
- Automated evaluation (LLM-as-a-Judge)
- Multi-dimensional scoring
- Continuous monitoring
- A/B testing framework
- Performance metrics tracking

### 4. **Production Considerations**
- Cost optimization (token usage)
- Latency management (<2s target)
- Error handling and retries
- Fallback mechanisms
- Conversation context management

## 💡 Key Concepts Explained

### Temperature Settings

Different tasks need different creativity levels:
- **0.1-0.3**: Categorization, safety checks (need consistency)
- **0.5-0.6**: Refunds, orders (balance accuracy and natural language)
- **0.7-0.8**: Generic inquiries (more conversational)

### Guardrails Layer

**Why it's critical:**
- LLMs can hallucinate or make up information
- May expose sensitive data (PII)
- Could make promises outside policy
- Might use inappropriate language

**Production implementation:**
```python
response = llm.generate(customer_message)
if not guardrails.is_safe(response):
    escalate_to_human()
else:
    send_to_customer(response)
```

### LLM-as-a-Judge

**Use cases:**
1. **Quality monitoring**: Evaluate 100% of responses automatically
2. **A/B testing**: Compare different prompt versions
3. **Training data**: Flag examples for fine-tuning
4. **Alerting**: Detect quality degradation early

**Metrics to track:**
- Relevance (answers the question?)
- Clarity (easy to understand?)
- Empathy (appropriate tone?)
- Completeness (all info provided?)
- Actionability (clear next steps?)

## 🔧 Customization

### Adding New Use Cases

1. **Create a new prompt in `src/prompts.py`**
2. **Add a method in `src/llm_service.py`**
3. **Create a new tab in `app.py`**

### Modifying Prompts

Edit `src/prompts.py` to adjust:
- Tone and style
- Policy details
- Response structure
- Evaluation criteria

### Changing Models

In `src/llm_service.py`, modify the default model:
```python
# Default: gpt-4o-mini (fast, cost-effective)
# Alternative: gpt-4o (more capable, higher cost)
```

## 📊 Cost Estimation

Using **gpt-4o-mini** (recommended):
- Input: ~$0.15 per 1M tokens
- Output: ~$0.60 per 1M tokens

**Typical usage:**
- Categorization: ~100 tokens
- Response generation: ~300-500 tokens
- Guardrails check: ~200 tokens
- Evaluation: ~400 tokens

**Example:** Processing 1,000 support tickets with full pipeline:
- Cost: ~$0.50-$1.00
- Compare to: Human agent costs ($15-30/hour)

## 🚨 Common Issues & Solutions

### Issue: "API Key Invalid"
**Solution:** Make sure you've entered a valid OpenAI API key with billing enabled

### Issue: "Rate Limit Error"
**Solution:** Reduce frequency of requests or upgrade your OpenAI plan

### Issue: "Slow Response Times"
**Solution:** 
- Switch to gpt-4o-mini if using gpt-4
- Reduce max_tokens parameter
- Use streaming responses (advanced)

## 🔒 Security Notes

- **Never commit API keys** to version control
- **Use environment variables** for sensitive data
- **Implement rate limiting** in production
- **Log and monitor** all API calls
- **Validate user inputs** before sending to LLM

## 🎯 Production Deployment Checklist

Before deploying to production:

- [ ] Implement proper authentication
- [ ] Set up monitoring and alerting
- [ ] Add rate limiting per user
- [ ] Configure error tracking (e.g., Sentry)
- [ ] Set up logging infrastructure
- [ ] Implement response caching
- [ ] Add database for conversation history
- [ ] Configure auto-scaling
- [ ] Set up A/B testing framework
- [ ] Implement human escalation workflow
- [ ] Add customer feedback collection
- [ ] Configure compliance logging
- [ ] Set up cost monitoring and budgets

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new use cases
- Improve prompts
- Enhance the UI
- Add more evaluation metrics

## 📝 License

This project is for educational purposes.

## 💬 Support

For questions about:
- **The application**: Check the code comments and this README
- **OpenAI API**: Visit OpenAI's documentation
- **Prompt engineering**: See the educational content in the sidebar

---

**Built with ❤️ for teaching production-grade LLM applications**

*Remember: This is a demonstration. Real production systems need additional security, monitoring, and infrastructure.*