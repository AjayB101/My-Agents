from langchain_core.prompts import PromptTemplate
from llm_client import llm
from tool_prompts import ToolPrompts


def generate_error_response(error_message: str, code_snippet: str = ""):
    prompt = ToolPrompts.generate_debug_prompt_template()
    chain = prompt | llm

    response = chain.invoke({
        "error_message": error_message,
        "code_snippet": code_snippet if code_snippet else "[No code provided]"
    })

    print(response.content)
    return response.content
