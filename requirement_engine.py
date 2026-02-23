"""
Requirement Engine Module - Member 1
=====================================
Processes raw business requirements into structured JSON and compares requirements.
"""

import json
import os
from typing import Dict, List, Any, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class RequirementProcessor:
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.3-70b-versatile"
        else:
            self.client = None

    def extract_requirement(self, raw_text: str) -> Dict[str, Any]:
        """Convert raw requirements into structured JSON using Advanced Spec."""
        if not self.client:
            return {
                "feature_name": "Sample Feature",
                "actors": ["User"],
                "functional_fields": ["Field1"],
                "validations": {"Field1": "Required"},
                "business_rules": ["Rule 1"],
                "edge_cases": ["Edge 1"],
                "risk_analysis": {
                    "high_risk_areas": ["Validation"],
                    "ambiguities": ["None"],
                    "missing_requirements": ["None"]
                }
            }

        prompt = f"""
You are an AI QA Architect with expert-level skills. Transform the raw requirement into a QA intelligence bundle.

PHASE 1 — ADVANCED REQUIREMENT UNDERSTANDING
Analyze the requirement deeply and extract:
1. feature_name  
2. actors (all user roles)  
3. functional_fields (every input field, even implied ones)  
4. validations (field -> rule). Include explicit and implied (e.g., "email" -> valid format)
5. business_rules  
6. edge_cases  
7. risk_analysis:
   - "high_risk_areas"
   - "ambiguities"
   - "missing_requirements"

IMPORTANT:
- ALWAYS output pure JSON, no markdown, no quotes outside JSON.
- If something is implied, infer it intelligently (e.g., email -> must be valid).
- If requirement is short, expand meaningfully using industry standards.

Requirement:
{raw_text}

Return output ONLY as STRICT valid JSON without commentary or markdown using this structure:
{{
  "feature_name": "",
  "actors": [],
  "functional_fields": [],
  "validations": {{}},
  "business_rules": [],
  "edge_cases": [],
  "risk_analysis": {{
      "high_risk_areas": [],
      "ambiguities": [],
      "missing_requirements": []
  }}
}}
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def compare_requirements(self, old_requirement: str, new_requirement: str) -> Dict[str, Any]:
        """Compare two versions of a requirement using Advanced Spec."""
        if not self.client:
            return {
                "added_fields": [],
                "removed_fields": [],
                "modified_validations": [],
                "added_rules": [],
                "removed_rules": [],
                "modified_rules": [],
                "risk_increase": [],
                "impact_analysis_summary": ""
            }

        prompt = f"""
You are an AI Requirement Change Detection Engine.

Compare OLD and NEW requirements and detect:
1. added_fields  
2. removed_fields  
3. modified_validations  
4. added_rules  
5. removed_rules  
6. modified_rules  
7. risk_increase  
8. impact_analysis_summary

IMPORTANT:
- ALWAYS output pure JSON, no markdown, no quotes outside JSON.
- If NEW requirement contains ANY new noun, treat as new field.

Return output ONLY as STRICT valid JSON without commentary or markdown in this structure:
{{
  "added_fields": [],
  "removed_fields": [],
  "modified_validations": [],
  "added_rules": [],
  "removed_rules": [],
  "modified_rules": [],
  "risk_increase": [],
  "impact_analysis_summary": ""
}}

OLD REQUIREMENT:
{old_requirement}

NEW REQUIREMENT:
{new_requirement}
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}


# Wrapper functions for app.py
def extract_requirement(raw_text: str) -> Dict[str, Any]:
    processor = RequirementProcessor()
    return processor.extract_requirement(raw_text)

def compare_requirements(old_req: str, new_req: str) -> Dict[str, Any]:
    processor = RequirementProcessor()
    return processor.compare_requirements(old_req, new_req)
