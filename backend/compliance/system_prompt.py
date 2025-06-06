# TODO: add compliance system prompt
COMPLIANCE_SYSTEM_PROMPT = """
You are a helpful assistant that checks compliance with regulations.
"""


class SystemPromptProvider:
    def get_system_prompt(self, system_prompt_type: str, custom_prompt: str):
        if system_prompt_type == "chat":
            return None
        elif system_prompt_type == "compliance":
            return COMPLIANCE_SYSTEM_PROMPT
        else:
            return custom_prompt
