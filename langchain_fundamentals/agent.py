import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Optional


class PhoneNumber(BaseModel):
    name: str
    phone: Optional[str] = None


class PhoneExtractionAgent:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY env var.")
        
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=model,
            temperature=0,
            stream=True
        )
        
        self.prompt = PromptTemplate(
            template="""You are a data extraction assistant. Extract phone numbers from the given text.

Extract ALL phone numbers found in the text below. For each person, return their name and phone number.

Text:
{text}

Return the results in the following format:
- Name: <person name>
  Phone: <phone number or "Not found">

If no phone number is found for a person, state "Not found".""",
            input_variables=["text"]
        )
    
    def extract(self, name: str = None, text: str = None) -> str:
        """Synchronous extraction"""
        if name:
            prompt_with_name = self.prompt.format(text=text) + f"\n\nSpecifically find the phone number for {name}."
            chain = self.llm
        else:
            prompt_with_name = self.prompt.format(text=text)
            chain = self.llm
        
        response = chain.invoke(prompt_with_name)
        return response.content
    
    def extract_stream(self, name: str = None, text: str = None):
        """Streaming extraction - yields chunks as they come"""
        if name:
            prompt_with_name = self.prompt.format(text=text) + f"\n\nSpecifically find the phone number for {name}."
            chain = self.llm
        else:
            prompt_with_name = self.prompt.format(text=text)
            chain = self.llm
        
        for chunk in chain.stream(prompt_with_name):
            if chunk.content:
                yield chunk.content
    
    def extract_all_phones(self, text: str):
        """Extract all phone numbers from text"""
        prompt = self.prompt.format(text=text)
        response = self.llm.invoke(prompt)
        return response.content
