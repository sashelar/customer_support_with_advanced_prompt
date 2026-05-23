# 🚀 Quick Reference Card

## Starting the Application

```bash
# Option 1: Using the start script
./start.sh

# Option 2: Manual start
pip install -r requirements.txt
streamlit run app.py
```

## Essential URLs

- **Local App**: http://localhost:8501
- **OpenAI API Keys**: https://platform.openai.com/api-keys
- **OpenAI Pricing**: https://openai.com/pricing

## Project Structure

```
customer_support_ai/
├── app.py                    # Main application
├── src/
│   ├── prompts.py           # All prompt templates
│   └── llm_service.py       # OpenAI integration
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Key Features by Tab

| Tab | Purpose | Key Prompt Technique |
|-----|---------|---------------------|
| 🏷️ Categorization | Route requests | Low temperature (0.3) |
| 💬 Generic Inquiry | Answer questions | Conversational prompts |
| 💰 Refund Request | Policy-based decisions | Context injection |
| 📦 Order Status | Track orders | Structured data |
| 📋 Policy Query | Explain policies | Clear formatting |
| 😟 Complaint | De-escalation | Empathy + solution |
| 🛡️ Guardrails | Safety checks | Critical validation |
| ⚖️ LLM-as-a-Judge | Quality evaluation | Multi-dimensional scoring |

## Prompt Engineering Cheat Sheet

### Temperature Guide
- **0.0-0.3**: Factual, consistent (categorization, safety)
- **0.4-0.6**: Balanced (refunds, orders, policies)
- **0.7-0.9**: Creative (complaints, empathy)

### Prompt Structure Best Practices
1. **Role**: Define the AI's role clearly
2. **Context**: Provide relevant information
3. **Task**: Specific instructions
4. **Constraints**: Limitations and rules
5. **Format**: Desired output structure
6. **Examples**: Show what you want (few-shot)

### Common Prompt Patterns

#### Classification
```
Analyze this {input} and categorize it as ONE of:
- Category A: description
- Category B: description
Format: CATEGORY | Explanation
```

#### Response Generation
```
You are a {role} for {company}.
Customer: {message}
Context: {relevant_data}

Provide a response that:
1. Point one
2. Point two
Response:
```

#### Evaluation
```
Evaluate this {output} on:
1. Dimension A (1-5)
2. Dimension B (1-5)
Format:
DIMENSION: score - justification
```

## Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| API key error | Check key is valid and has billing enabled |
| Rate limit | Wait or upgrade OpenAI plan |
| Slow responses | Switch to gpt-4o-mini model |
| Module not found | Run `pip install -r requirements.txt` |
| Port already in use | Use `streamlit run app.py --server.port 8502` |

## Cost Optimization Tips

1. **Use gpt-4o-mini** for most tasks (10x cheaper than GPT-4)
2. **Limit max_tokens** to reduce output costs
3. **Cache responses** for repeated queries
4. **Batch requests** when possible
5. **Monitor usage** with OpenAI dashboard

## Production Checklist

### Must-Have
- [ ] Guardrails validation
- [ ] Error handling
- [ ] Rate limiting
- [ ] Logging and monitoring
- [ ] Human escalation path

### Should-Have
- [ ] Response caching
- [ ] A/B testing framework
- [ ] Quality metrics dashboard
- [ ] Cost monitoring
- [ ] Customer feedback loop

### Nice-to-Have
- [ ] Fine-tuned models
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Predictive routing
- [ ] Sentiment analysis

## Key Metrics to Track

### Quality Metrics
- Response relevance score
- Customer satisfaction (CSAT)
- First contact resolution rate
- Escalation rate to humans

### Performance Metrics
- Average response time
- Throughput (requests/second)
- Error rate
- API uptime

### Cost Metrics
- Cost per interaction
- Token usage per category
- ROI vs human support
- Monthly API spend

## Industry Benchmarks

| Metric | Target | World-Class |
|--------|--------|-------------|
| Automation Rate | 60-70% | 80%+ |
| Response Time | <3s | <2s |
| CSAT Score | 80%+ | 90%+ |
| Cost per Ticket | $0.50 | $0.10 |

## Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run with specific port
streamlit run app.py --server.port 8502

# Clear Streamlit cache
streamlit cache clear

# Check OpenAI API status
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

## Learning Resources

### Documentation
- OpenAI API: https://platform.openai.com/docs
- Streamlit: https://docs.streamlit.io
- Prompt Engineering: https://learn.prompting.org

### Best Practices
- Anthropic's Prompt Engineering Guide
- OpenAI's GPT Best Practices
- LangChain Documentation

### Community
- r/PromptEngineering
- OpenAI Developer Forum
- Streamlit Community Forum

## Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini  # Optional override
MAX_TOKENS=500          # Optional override
TEMPERATURE=0.7         # Optional override
```

## Debugging Tips

### Check Logs
```python
# Add to llm_service.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Prompts
```python
# Quick test outside app
from src.llm_service import LLMService
from src.prompts import CATEGORIZATION_PROMPT

llm = LLMService(api_key="your-key")
result = llm.categorize_request("test message", CATEGORIZATION_PROMPT)
print(result)
```

### Monitor API Calls
- Use OpenAI Dashboard: https://platform.openai.com/usage
- Track token usage in app (shown in sidebar)
- Enable verbose logging for debugging

## Contact & Support

- **GitHub Issues**: [Report bugs or request features]
- **Documentation**: See README.md
- **API Support**: https://help.openai.com

---

**Pro Tip**: Start with the sample messages, then create your own test cases. The best way to learn prompt engineering is by experimenting! 🚀
