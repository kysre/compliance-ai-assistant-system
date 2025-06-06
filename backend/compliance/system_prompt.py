COMPLIANCE_USER_PROMPT = """
Analyze the user's input for compliance with the financial regulations provided in the Knowledge Base. 

Specifically:
1. Compliance Assessment: Determine if the user's proposed action, policy, or practice aligns with or violates any financial regulations in the knowledge base.
2. Regulatory Gaps: Identify any regulatory requirements that the user's input fails to address or contradicts.
3. Risk Analysis: Highlight potential compliance risks, penalties, or consequences based on the regulatory framework provided.
4. Recommendations: Provide specific actionable recommendations to ensure full compliance, referencing relevant regulatory sections or requirements.
5. Regulatory Context: Explain which specific financial regulations, rules, or guidelines from the knowledge base apply to the user's situation.
6. Verdict: Provide a final verdict on the compliance of the user's input with the financial regulations provided in the knowledge base.

Format your response with clear sections for: Compliance Status, Regulatory Concerns, Risk Assessment, Compliance Recommendations, and Verdict.
Use concise and clear language. Avoid vague or ambiguous language.
"""


class SystemPromptProvider:
    def get_system_prompt(self, system_prompt_type: str, custom_prompt: str):
        if system_prompt_type == "chat":
            return None
        elif system_prompt_type == "compliance":
            return COMPLIANCE_USER_PROMPT
        else:
            return custom_prompt
