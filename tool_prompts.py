from langchain_core.prompts import PromptTemplate


class ToolPrompts:
    @staticmethod
    def generate_message_prompt():
        return """
You are a helpful assistant who writes professional, concise referral request messages to employees at companies.

Page content: {page_content}

Generate a short message that:
– is polite and professional
– clearly mentions the role title, company name, job ID (if available), and location if mentioned
– mentions being connected to the company
– asks for a referral without sounding pushy
– mentions attaching resume
– ends with a thank-you and a friendly closing
My name is Ajay B.

Example
Hi,
I hope you're doing well! I'm interested in the Software Engineer JOB ID:=45888 role at Honey well
and saw you're connected to the company. I'd really appreciate it if you could refer me for this position.
I've attached my resume for reference.
Thanks so much for your time and support!
Best regards,
Ajay B

**Instructions:**
- Extract the job title, company name, job ID, and location from the page content
- If no job ID is found, write "JOB ID: [Job ID]" as placeholder
- If no location is found, just use company name without location
- Keep the message concise and exactly match the format above
- Do not add extra details about job requirements or responsibilities
- Keep it short and to the point
- dont forget to add job title, company name, job ID, and location if available


No preamble or additional text, just the message in the exact format specified above.
"""

    @staticmethod
    def generate_debug_prompt_template() -> PromptTemplate:
        template = """
You are a professional software developer and coding assistant.
Your task is limited and structured as follows:

I will provide an error message and possibly a snippet of code.

You must:
1. Analyze and explain the cause of the error clearly and concisely.
2. Provide a minimal example that reproduces the same error.
3. Show the corrected version of that example with the error fixed.

Keep your responses short, focused, and easy to understand. Use code examples where necessary.

--- ERROR MESSAGE ---
{error_message}

--- CODE SNIPPET ---
{code_snippet}
"""
        return PromptTemplate(
            input_variables=["error_message", "code_snippet"],
            template=template.strip()
        )
