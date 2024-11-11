import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains.llm_math.base import LLMMathChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

## Setup API Streamlit app
st.set_page_config("Text to Math Problem Solver and Data search Asistant", page_icon="💢")
st.title("Text to amth problem Solver with Gamma2")

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please Add Your Groq API Key to Continue.")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key= groq_api_key)

##Initializing the tool
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="wikipedia",
    func= wikipedia_wrapper.run(),
    description= "A tool for searching the internet to find the various information on the given question"
)

#Initializing Math Tool
math_chain = LLMMathChain(llm=llm)
calculator= Tool(
    name="calculator",
    func=math_chain.run(),
    description="A Tool for answering math related questions.only input mathematical expression need to be provided."
) 

prompt = """
You are agent solving users mathematical questions. Logically arrive at the solutions and provide a detail explanations
and display it point wise at the below questions
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combining all the tools into chain
chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

reasoning_tool = Tool(
    name= "Reasoning tool",
    func=chain.run()
    description= "A tool for answering logic-based and reasoning questions."

)

