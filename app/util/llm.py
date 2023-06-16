import os
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import openai

from app.constant.prompt_templates import GENERIC_TEMPLATE_USER,GENERIC_TEMPLATE_SYSTEM


def make_llm_call(input,framework,directory_structure,model_name):
        system_template = GENERIC_TEMPLATE_SYSTEM.format(framework=framework)
        user_template  = GENERIC_TEMPLATE_USER.format(input_file=input,directory_structure=directory_structure)
        messages = [
            {"role": "system", "content": system_template},
            {"role": "user", "content": user_template},
        ]
        response = openai.ChatCompletion.create(
            model=model_name.lower(),
            messages=messages,
            temperature=0,
            stop="'''"
        )

        generated_texts = [
            choice.message["content"].strip() for choice in response["choices"]
        ]

        return generated_texts


def make_llm_call_langchain(input,framework,directory_structure,model_name):
        # system_template = GENERIC_TEMPLATE_SYSTEM.format(framework=framework)
        # user_template  = GENERIC_TEMPLATE_USER.format(input_file=input,directory_structure=directory_structure)
        
        # llm = ChatOpenAI(model_name=model_name.lower(),temperature=0,stop="'''",verbose=True)
        # messages = [
        #     SystemMessage(content=system_template),
        #     HumanMessage(content=user_template)
        # ]
        # res = llm(messages)
        # return res.content

        llm = ChatOpenAI(model_name=model_name.lower(),temperature=0)

        system_message_prompt = SystemMessagePromptTemplate.from_template(GENERIC_TEMPLATE_SYSTEM)
        human_message_prompt = HumanMessagePromptTemplate.from_template(GENERIC_TEMPLATE_USER)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=llm, prompt=chat_prompt,verbose=True)
        res = chain.run(framework=framework,input_file=input,directory_structure=directory_structure)
        return res
