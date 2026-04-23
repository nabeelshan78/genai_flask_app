def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq model cleanly
llama_llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=256
)

# Define JSON output structure
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

# JSON output parser
json_parser = JsonOutputParser(pydantic_object=AIResponse)

# Prompt template streamlined for Groq/Llama-3
llama_template = PromptTemplate(
    template="System: {system_prompt}\n{format_prompt}\nHuman: {user_prompt}\nAI:",
    input_variables=["system_prompt", "user_prompt"],
    partial_variables={"format_prompt": json_parser.get_format_instructions()}
)

def groq_response(system_prompt, user_prompt):
    chain = llama_template | llama_llm | json_parser
    return chain.invoke({'system_prompt': system_prompt, 'user_prompt': user_prompt})