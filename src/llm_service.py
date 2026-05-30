"""
LLM Service Module
Handles all interactions with OpenAI API
"""

from openai import OpenAI
import os
from typing import Dict, Optional
import time


class LLMService:
    """Service class for interacting with OpenAI's LLM"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM service
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.call_count = 0
        
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict:
        """
        Generate a response from the LLM
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary containing response and metadata
        """
        self.call_count += 1
        start_time = time.time()
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            elapsed_time = time.time() - start_time
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "elapsed_time": elapsed_time,
                "call_number": self.call_count
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "call_number": self.call_count
            }
    
    def categorize_request(self, customer_message: str, categorization_prompt: str) -> Dict:
        """Categorize a customer support request"""
        prompt = categorization_prompt.format(customer_message=customer_message)
        return self.generate_response(prompt, temperature=0.3)
    
    def handle_inquiry(self, customer_message: str, inquiry_prompt: str, system_prompt: str) -> Dict:
        """Handle a generic inquiry"""
        prompt = inquiry_prompt.format(customer_message=customer_message)
        return self.generate_response(prompt, system_prompt=system_prompt, temperature=0.7)
    
    def handle_refund(
        self, 
        customer_message: str, 
        order_details: str, 
        refund_prompt: str,
        system_prompt: str
    ) -> Dict:
        """Handle a refund request"""
        prompt = refund_prompt.format(
            customer_message=customer_message,
            order_details=order_details
        )
        return self.generate_response(prompt, system_prompt=system_prompt, temperature=0.5)
    
    def handle_order_status(
        self,
        customer_message: str,
        order_info: str,
        status_prompt: str,
        system_prompt: str
    ) -> Dict:
        """Handle an order status query"""
        prompt = status_prompt.format(
            customer_message=customer_message,
            order_info=order_info
        )
        return self.generate_response(prompt, system_prompt=system_prompt, temperature=0.5)
    
    def handle_policy(
        self,
        customer_message: str,
        policy_context: str,
        policy_prompt: str,
        system_prompt: str
    ) -> Dict:
        """Handle a policy query"""
        prompt = policy_prompt.format(
            customer_message=customer_message,
            policy_context=policy_context
        )
        return self.generate_response(prompt, system_prompt=system_prompt, temperature=0.5)
    
    def handle_complaint(
        self,
        customer_message: str,
        issue_type: str,
        complaint_prompt: str,
        system_prompt: str
    ) -> Dict:
        """Handle a customer complaint"""
        prompt = complaint_prompt.format(
            customer_message=customer_message,
            issue_type=issue_type
        )
        return self.generate_response(prompt, system_prompt=system_prompt, temperature=0.6)
    
    def check_guardrails(self, response: str, guardrails_prompt: str) -> Dict:
        """
        Check if a response is safe and compliant
        
        This is a critical production consideration - always validate LLM outputs
        before showing them to customers
        """
        prompt = guardrails_prompt.format(response=response)
        return self.generate_response(prompt, temperature=0.1, max_tokens=400)
    
    def evaluate_response(
        self,
        customer_message: str,
        ai_response: str,
        judge_prompt: str
    ) -> Dict:
        """
        Use LLM-as-a-Judge to evaluate the quality of a response
        
        This technique is widely used in production to:
        1. Monitor response quality
        2. A/B test different prompts
        3. Identify areas for improvement
        4. Create training datasets for fine-tuning
        """
        prompt = judge_prompt.format(
            customer_message=customer_message,
            ai_response=ai_response
        )
        return self.generate_response(prompt, temperature=0.2, max_tokens=600)
    
    def classify_ticket(self, ticket_message: str, prompt_messages: list) -> Dict:
        """Classify a support ticket using a pre-built messages array (zero-shot or few-shot)."""
        self.call_count += 1
        start_time = time.time()
        try:
            messages = prompt_messages + [{"role": "user", "content": ticket_message}]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,
                max_tokens=20
            )
            elapsed_time = time.time() - start_time
            return {
                "success": True,
                "response": response.choices[0].message.content.strip(),
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "elapsed_time": elapsed_time,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def summarize_legal_doc(self, doc_text: str, system_message: str, few_shot_examples: list = None) -> Dict:
        """Summarize a legal document using few-shot prompting."""
        self.call_count += 1
        start_time = time.time()
        try:
            messages = [{"role": "developer", "content": system_message}]
            if few_shot_examples:
                messages.extend(few_shot_examples)
            messages.append({"role": "user", "content": doc_text})
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=300
            )
            elapsed_time = time.time() - start_time
            return {
                "success": True,
                "response": response.choices[0].message.content.strip(),
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "elapsed_time": elapsed_time,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def judge_legal_summary(self, legal_doc: str, summary: str, judge_system: str, user_template: str) -> Dict:
        """Use LLM-as-a-Judge to evaluate a legal document summary."""
        self.call_count += 1
        start_time = time.time()
        try:
            user_content = user_template.format(legal_doc=legal_doc, summary=summary)
            messages = [
                {"role": "developer", "content": judge_system},
                {"role": "user", "content": user_content},
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,
                max_tokens=600
            )
            elapsed_time = time.time() - start_time
            return {
                "success": True,
                "response": response.choices[0].message.content.strip(),
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "elapsed_time": elapsed_time,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            "total_calls": self.call_count,
            "model": self.model
        }
