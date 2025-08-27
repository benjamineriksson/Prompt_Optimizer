"""
4-D Prompt Optimizer
Enhanced prompt optimization using the proven 4-D methodology
"""

import openai
from openai import OpenAI
import logging
from datetime import datetime
import os
import json
import requests
from typing import Dict, List, Optional
from config import Config

# Configure logging
logger = logging.getLogger(__name__)

class PromptOptimizer:
    def __init__(self):
        self.config = Config()
        self.config.validate_config()
        
        # 4-D methodology to be embedded in DeepSeek API calls
        self.methodology = """
You are an expert prompt optimization AI. Apply the 4-D METHODOLOGY to optimize user prompts:

THE 4-D METHODOLOGY:
1. DECONSTRUCT
   - Extract core intent, key entities, and context
   - Identify output requirements and constraints
   - Map what's provided vs. what's missing

2. DIAGNOSE
   - Audit for clarity gaps and ambiguity
   - Check specificity and completeness
   - Assess structure and complexity needs

3. DEVELOP
   - Select optimal techniques based on request type:
     * Creative → Multi-perspective + tone emphasis
     * Technical → Constraint-based + precision focus
     * Educational → Few-shot examples + clear structure
     * Complex → Chain-of-thought + systematic frameworks
   - Assign appropriate AI role/expertise
   - Enhance context and implement logical structure

4. DELIVER
   - Construct optimized prompt
   - Format based on complexity
   - Provide implementation guidance

OPTIMIZATION TECHNIQUES:
- Foundation: Role assignment, context layering, output specs, task decomposition
- Advanced: Chain-of-thought, few-shot learning, multi-perspective analysis, constraint optimization

OPERATING MODES:
DETAIL MODE:
- Gather context with smart defaults
- Ask 2-3 targeted clarifying questions
- Provide comprehensive optimization

BASIC MODE:
- Quick fix primary issues
- Apply core techniques only
- Deliver ready-to-use prompt

RESPONSE FORMATS:
For Simple Requests:
**Your Optimized Prompt:**
[Improved prompt]

**What Changed:** [Key improvements]

For Complex Requests:
**Your Optimized Prompt:**
[Improved prompt]

**Key Improvements:**
• [Primary changes and benefits]

**Techniques Applied:** [Brief mention]

**Pro Tip:** [Usage guidance]
"""

    def optimize_prompt(self, raw_prompt: str, prompt_style: str, target_ai: str) -> Dict:
        """
        Optimize a prompt using the 4-D methodology via DeepSeek API
        
        Args:
            raw_prompt: The user's original prompt
            prompt_style: "BASIC" or "DETAIL"
            target_ai: "ChatGPT", "Claude", "Gemini", or "Other"
            
        Returns:
            Dict containing optimized prompt and metadata
        """
        try:
            # Construct the DeepSeek API payload
            messages = [
                {
                    "role": "system",
                    "content": self.methodology
                },
                {
                    "role": "user",
                    "content": self._build_user_message(raw_prompt, prompt_style, target_ai)
                }
            ]
            
            # Select model based on complexity
            model = self.config.REASONING_MODEL if prompt_style == "DETAIL" else self.config.DEFAULT_MODEL
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }
            
            # Make API call to DeepSeek
            response = self._call_deepseek_api(payload)
            
            # Parse and format the response
            return self._parse_response(response)
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Optimization failed: {str(e)}",
                "optimized_prompt": None
            }
    
    def _build_user_message(self, raw_prompt: str, prompt_style: str, target_ai: str) -> str:
        """Build the user message for the DeepSeek API call"""
        return f"""
Please optimize the following prompt using the {prompt_style} mode approach, targeting {target_ai}:

Raw Prompt: {raw_prompt}

Optimization Style: {prompt_style}
Target AI: {target_ai}

Apply your 4-D methodology and provide the response in the appropriate format based on the complexity of the request.
"""
    
    def _call_deepseek_api(self, payload: Dict) -> Dict:
        """Make the actual API call to DeepSeek"""
        headers = {
            "Authorization": f"Bearer {self.config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            self.config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def _parse_response(self, api_response: Dict) -> Dict:
        """Parse the DeepSeek API response and extract components"""
        try:
            content = api_response['choices'][0]['message']['content']
            
            # Parse the structured response from Lyra
            parsed = self._extract_components(content)
            
            return {
                "error": False,
                "optimized_prompt": parsed.get("optimized_prompt", content),
                "improvements": parsed.get("improvements", []),
                "techniques_applied": parsed.get("techniques_applied", []),
                "pro_tip": parsed.get("pro_tip", ""),
                "raw_response": content
            }
            
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to parse DeepSeek response: {str(e)}")
    
    def _extract_components(self, content: str) -> Dict:
        """Extract structured components from the optimization response"""
        components = {}
        
        # Extract optimized prompt
        if "**Your Optimized Prompt:**" in content:
            start = content.find("**Your Optimized Prompt:**") + len("**Your Optimized Prompt:**")
            end = content.find("**", start)
            if end == -1:
                end = content.find("\n\n", start)
            if end != -1:
                components["optimized_prompt"] = content[start:end].strip()
        
        # Extract improvements
        improvements = []
        if "**What Changed:**" in content:
            start = content.find("**What Changed:**") + len("**What Changed:**")
            end = content.find("**", start)
            if end != -1:
                improvements.append(content[start:end].strip())
        elif "**Key Improvements:**" in content:
            start = content.find("**Key Improvements:**") + len("**Key Improvements:**")
            end = content.find("**", start)
            if end != -1:
                improvements_text = content[start:end].strip()
                # Split by bullet points
                improvements = [imp.strip("• ").strip() for imp in improvements_text.split("•") if imp.strip()]
        
        components["improvements"] = improvements
        
        # Extract techniques applied
        if "**Techniques Applied:**" in content:
            start = content.find("**Techniques Applied:**") + len("**Techniques Applied:**")
            end = content.find("**", start)
            if end == -1:
                end = len(content)
            if end != -1:
                techniques_text = content[start:end].strip()
                components["techniques_applied"] = [techniques_text] if techniques_text else []
        
        # Extract pro tip
        if "**Pro Tip:**" in content:
            start = content.find("**Pro Tip:**") + len("**Pro Tip:**")
            end = len(content)
            components["pro_tip"] = content[start:end].strip()
        
        return components

    def health_check(self) -> Dict:
        """Check if the DeepSeek API is accessible"""
        try:
            # Simple test call
            payload = {
                "model": self.config.DEFAULT_MODEL,
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 10
            }
            
            self._call_deepseek_api(payload)
            return {"status": "healthy", "api_accessible": True}
            
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "api_accessible": False}
