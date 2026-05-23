"""
Enhanced LLM Service Module - Implements Advanced Prompt Engineering Techniques
Based on Week 2: Few-Shot, CoT, Rephrase & Respond, Self-Consistency, LLM-as-a-Judge
"""

from openai import OpenAI
import os
from typing import Dict, Optional, List
import time
import json


class EnhancedLLMService:
    """Enhanced service class with advanced prompt engineering techniques"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the enhanced LLM service
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.call_count = 0
        
    def generate_response(
        self, 
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        n: int = 1
    ) -> Dict:
        """
        Generate a response from the LLM
        
        Args:
            messages: List of message dicts with role and content
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            n: Number of completions to generate
            
        Returns:
            Dictionary containing response and metadata
        """
        self.call_count += 1
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=n
            )
            
            elapsed_time = time.time() - start_time
            
            # If multiple completions requested
            if n > 1:
                return {
                    "success": True,
                    "responses": [choice.message.content for choice in response.choices],
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "elapsed_time": elapsed_time,
                    "call_number": self.call_count
                }
            
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
    
    # ============================
    # FEW-SHOT LEARNING
    # ============================
    
    def few_shot_categorize(
        self,
        customer_message: str,
        system_message: str,
        examples: List[Dict]
    ) -> Dict:
        """
        Categorize using few-shot prompting
        
        Examples show the model the expected format
        """
        messages = [{"role": "developer", "content": system_message}]
        messages.extend(examples)
        messages.append({"role": "user", "content": customer_message})
        
        return self.generate_response(messages, temperature=0.3, max_tokens=200)
    
    def few_shot_sentiment(
        self,
        review_text: str,
        system_message: str,
        examples: List[Dict]
    ) -> Dict:
        """
        Sentiment analysis using few-shot learning
        """
        messages = [{"role": "developer", "content": system_message}]
        messages.extend(examples)
        messages.append({"role": "user", "content": review_text})
        
        return self.generate_response(messages, temperature=0, max_tokens=100)
    
    # ============================
    # CHAIN-OF-THOUGHT (CoT)
    # ============================
    
    def cot_entity_extraction(
        self,
        customer_complaint: str,
        system_message: str
    ) -> Dict:
        """
        Extract entities using chain-of-thought reasoning
        
        The prompt asks the model to explain its reasoning step-by-step
        """
        messages = [
            {"role": "developer", "content": system_message},
            {"role": "user", "content": customer_complaint}
        ]
        
        return self.generate_response(messages, temperature=0, max_tokens=800)
    
    def cot_refund_analysis(
        self,
        customer_complaint: str,
        system_message: str
    ) -> Dict:
        """
        Analyze refund requests with step-by-step reasoning
        """
        messages = [
            {"role": "developer", "content": system_message},
            {"role": "user", "content": customer_complaint}
        ]
        
        return self.generate_response(messages, temperature=0.2, max_tokens=1000)
    
    # ============================
    # TWO-STAGE CHAIN-OF-THOUGHT
    # ============================
    
    def two_stage_cot(
        self,
        customer_feedback: str,
        stage1_system: str,
        stage2_system: str
    ) -> Dict:
        """
        Two-stage CoT: First analyze, then generate recommendations
        
        This breaks complex tasks into manageable steps
        """
        # Stage 1: Analysis
        stage1_messages = [
            {"role": "developer", "content": stage1_system},
            {"role": "user", "content": customer_feedback}
        ]
        
        stage1_result = self.generate_response(stage1_messages, temperature=0, max_tokens=600)
        
        if not stage1_result["success"]:
            return stage1_result
        
        # Stage 2: Recommendations based on Stage 1 output
        stage2_messages = [
            {"role": "developer", "content": stage2_system},
            {"role": "user", "content": f"Analysis from Stage 1:\n\n{stage1_result['response']}"}
        ]
        
        stage2_result = self.generate_response(stage2_messages, temperature=0, max_tokens=800)
        
        # Combine results
        return {
            "success": stage2_result["success"],
            "stage1_analysis": stage1_result["response"],
            "stage2_recommendations": stage2_result.get("response", ""),
            "total_tokens": stage1_result["tokens_used"] + stage2_result.get("tokens_used", 0),
            "total_time": stage1_result["elapsed_time"] + stage2_result.get("elapsed_time", 0)
        }
    
    # ============================
    # SELF-CONSISTENCY
    # ============================
    
    def self_consistency(
        self,
        question: str,
        context: str,
        generation_system: str,
        selection_system: str,
        num_generations: int = 3
    ) -> Dict:
        """
        Generate multiple answers and select the most consistent one
        
        Useful for factual questions where accuracy matters
        """
        # Stage 1: Generate multiple answers
        formatted_system = generation_system.format(context=context)
        
        gen_messages = [
            {"role": "developer", "content": formatted_system},
            {"role": "user", "content": question}
        ]
        
        gen_result = self.generate_response(
            gen_messages,
            temperature=0.7,  # Higher temp for diverse answers
            max_tokens=600,
            n=num_generations
        )
        
        if not gen_result["success"]:
            return gen_result
        
        # Extract the multiple responses
        multiple_answers = gen_result["responses"]
        
        # Stage 2: Select most consistent answer
        selection_input = f"""Question: {question}

Generated Answers:
{chr(10).join([f"{i+1}. {ans}" for i, ans in enumerate(multiple_answers)])}"""
        
        selection_messages = [
            {"role": "developer", "content": selection_system},
            {"role": "user", "content": selection_input}
        ]
        
        selection_result = self.generate_response(
            selection_messages,
            temperature=0,  # Low temp for deterministic selection
            max_tokens=400
        )
        
        return {
            "success": selection_result["success"],
            "generated_answers": multiple_answers,
            "selected_answer": selection_result.get("response", ""),
            "total_tokens": gen_result["tokens_used"] + selection_result.get("tokens_used", 0),
            "num_generations": num_generations
        }
    
    # ============================
    # REPHRASE & RESPOND
    # ============================
    
    def rephrase_and_respond(
        self,
        question: str,
        context: str,
        rephrase_system: str,
        respond_system: str
    ) -> Dict:
        """
        First rephrase the question for clarity, then answer
        
        This helps the model better understand ambiguous questions
        """
        # Stage 1: Rephrase the question
        rephrase_formatted = rephrase_system.format(context=context)
        
        rephrase_messages = [
            {"role": "developer", "content": rephrase_formatted},
            {"role": "user", "content": question}
        ]
        
        rephrase_result = self.generate_response(
            rephrase_messages,
            temperature=0.3,
            max_tokens=300
        )
        
        if not rephrase_result["success"]:
            return rephrase_result
        
        rephrased_question = rephrase_result["response"]
        
        # Stage 2: Answer using the rephrased question
        respond_formatted = respond_system.format(context=context)
        
        respond_input = f"""Original Question: {question}

Rephrased Question: {rephrased_question}"""
        
        respond_messages = [
            {"role": "developer", "content": respond_formatted},
            {"role": "user", "content": respond_input}
        ]
        
        respond_result = self.generate_response(
            respond_messages,
            temperature=0.5,
            max_tokens=500
        )
        
        return {
            "success": respond_result["success"],
            "original_question": question,
            "rephrased_question": rephrased_question,
            "final_answer": respond_result.get("response", ""),
            "total_tokens": rephrase_result["tokens_used"] + respond_result.get("tokens_used", 0)
        }
    
    # ============================
    # LLM-AS-A-JUDGE (Enhanced)
    # ============================
    
    def comprehensive_judge(
        self,
        customer_request: str,
        ai_response: str,
        judge_system: str
    ) -> Dict:
        """
        Comprehensive evaluation using LLM-as-a-judge
        
        Evaluates multiple dimensions with detailed rubrics
        """
        judge_input = f"""###Request
{customer_request}

###Response
{ai_response}"""
        
        judge_messages = [
            {"role": "developer", "content": judge_system},
            {"role": "user", "content": judge_input}
        ]
        
        result = self.generate_response(
            judge_messages,
            temperature=0.1,  # Very low for consistent evaluation
            max_tokens=1200
        )
        
        if result["success"]:
            try:
                # Try to parse JSON response
                eval_json = json.loads(result["response"].replace("```json", "").replace("```", "").strip())
                result["evaluation"] = eval_json
                result["parsed"] = True
            except:
                result["parsed"] = False
        
        return result
    
    # ============================
    # ZERO-SHOT (for comparison)
    # ============================
    
    def zero_shot_categorize(
        self,
        customer_message: str,
        system_message: str
    ) -> Dict:
        """
        Zero-shot categorization (no examples)
        
        For comparison with few-shot
        """
        messages = [
            {"role": "developer", "content": system_message},
            {"role": "user", "content": customer_message}
        ]
        
        return self.generate_response(messages, temperature=0.3, max_tokens=200)
    
    # ============================
    # UTILITIES
    # ============================
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            "total_calls": self.call_count,
            "model": self.model
        }
    
    def compare_temperatures(
        self,
        messages: List[Dict],
        temperatures: List[float] = [0, 0.4, 0.7, 1.0]
    ) -> Dict:
        """
        Compare outputs at different temperatures
        
        Educational tool to show temperature effects
        """
        results = {}
        
        for temp in temperatures:
            result = self.generate_response(
                messages,
                temperature=temp,
                max_tokens=500
            )
            results[f"temp_{temp}"] = result
        
        return results
