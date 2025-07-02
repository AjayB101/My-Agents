from langchain_core.prompts import PromptTemplate
from llm_client import llm
from tool_prompts import ToolPrompts


prompt = PromptTemplate(
    input_variables=["jd"], template=ToolPrompts.generate_message_prompt())
email_chain = prompt | llm


def generate_message(page_content: str):
    res = email_chain.invoke({"page_content": page_content})
    print(res.content)
    return res.content
