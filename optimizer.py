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

    def optimize_prompt(self, raw_prompt: str, prompt_style: str, target_ai: str, clarifications: Optional[str] = None) -> Dict:
        """
        Optimize a prompt using the 4-D methodology via DeepSeek API
        
        Args:
            raw_prompt: The user's original prompt
            prompt_style: "BASIC" or "DETAIL"
            target_ai: "ChatGPT", "Claude", "Gemini", or "Other"
            clarifications: Additional context from user (for DETAIL mode stage 2)
            
        Returns:
            Dict containing optimized prompt and metadata, or clarifying questions
        """
        try:
            # For DETAIL mode without clarifications, first ask questions
            if prompt_style == "DETAIL" and clarifications is None:
                return self._get_clarifying_questions(raw_prompt, target_ai)
            
            # For BASIC mode or DETAIL with clarifications, proceed with optimization
            messages = [
                {
                    "role": "system",
                    "content": self.methodology
                },
                {
                    "role": "user",
                    "content": self._build_user_message(raw_prompt, prompt_style, target_ai, clarifications)
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
                "error": str(e),
                "optimized_prompt": None,
                "improvements": [],
                "techniques_applied": [],
                "pro_tip": ""
            }

    def _get_clarifying_questions(self, raw_prompt: str, target_ai: str) -> Dict:
        """Get clarifying questions for DETAIL mode optimization"""
        try:
            question_system_prompt = """
You are an expert prompt optimization consultant. Your job is to analyze a user's prompt and ask 2-3 targeted clarifying questions to gather essential context for optimization.

ANALYSIS PROCESS:
1. DECONSTRUCT the prompt to identify gaps
2. DIAGNOSE what information is missing
3. ASK 2-3 specific questions that will improve the optimization

QUESTION GUIDELINES:
- Focus on PURPOSE, CONTEXT, CONSTRAINTS, or OUTPUT FORMAT
- Be specific and actionable
- Avoid generic questions
- Prioritize the most impactful clarifications

RESPONSE FORMAT:
**Analysis:** [Brief assessment of what's unclear or missing]

**Questions:**
1. [Specific question about purpose/context]
2. [Specific question about constraints/requirements]  
3. [Specific question about output/format] (if needed)

Keep it concise but insightful.
"""

            messages = [
                {
                    "role": "system", 
                    "content": question_system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Please analyze this prompt and ask clarifying questions for optimization targeting {target_ai}:

Raw Prompt: {raw_prompt}

Target AI: {target_ai}

What 2-3 questions would help me optimize this prompt most effectively?
"""
                }
            ]

            payload = {
                "model": self.config.DEFAULT_MODEL,
                "messages": messages,
                "temperature": 0.6,
                "max_tokens": 800,
                "stream": False
            }

            response = self._call_deepseek_api(payload)
            response_content = response['choices'][0]['message']['content']

            return {
                "needs_clarification": True,
                "questions": response_content,
                "optimized_prompt": None,
                "improvements": [],
                "techniques_applied": [],
                "pro_tip": "Please answer the questions above to get a comprehensive optimization."
            }

        except Exception as e:
            # Fallback to basic optimization if questions fail
            return self.optimize_prompt(raw_prompt, "BASIC", target_ai)
    
    def _build_user_message(self, raw_prompt: str, prompt_style: str, target_ai: str, clarifications: Optional[str] = None) -> str:
        """Build the user message for the DeepSeek API call"""
        base_message = f"""
Please optimize the following prompt using the {prompt_style} mode approach, targeting {target_ai}:

Raw Prompt: {raw_prompt}

Optimization Style: {prompt_style}
Target AI: {target_ai}"""

        if clarifications:
            base_message += f"""

Additional Context from User:
{clarifications}"""

        base_message += """

Apply your 4-D methodology and provide the response in the appropriate format based on the complexity of the request."""
        
        return base_message
    
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
