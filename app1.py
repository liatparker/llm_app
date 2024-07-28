

import streamlit as st
from langchain_openai import OpenAI

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.summarize import load_summarize_chain
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
#from langchain import OpenAI, PromptTemplate
import glob


def summarize_pdfs_from_folder(pdfs_folder):
    llm = OpenAI(temperature=0.2, openai_api_key=openai_api_key) 
    summaries = []
    for pdf_file in glob.glob(pdfs_folder + "/*.pdf"):
        loader = PyPDFLoader(pdf_file)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)
        print("Summary for: ", pdf_file)
        print(summary)
        print("\n")
        summaries.append(summary)

    return summaries


def custom_summary(pdf_folder, custom_prompt):
    summaries = []
    for pdf_file in glob.glob(pdf_folder + "/*.pdf"):
        loader = PyPDFLoader(pdf_file)
        docs = loader.load_and_split()
        prompt_template = custom_prompt + """

        {text}

        SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(llm, chain_type="map_reduce",
                                     map_prompt=PROMPT, combine_prompt=PROMPT)
        summary_output = chain({"input_documents": docs}, return_only_outputs=True)["output_text"]
        summaries.append(summary_output)

    return summaries

def generate_response(txt):
    # Instantiate the LLM model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    # Split text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)
    # Create multiple documents
    docs = [Document(page_content=t) for t in texts]
    # Text summarization
    chain = load_summarize_chain(llm, chain_type='map_reduce')
    return chain.run(docs)

# Page title
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

# Text input
#txt_input = st.text_area('Enter your text', '', height=200)
txt_input = st.text_area('Enter your pdf folder path', '', height=200)
# Form to accept user's text input for summarization
result = []
with st.form('summarize_form', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type = 'password', disabled=not txt_input)
    submitted = st.form_submit_button('Submit')
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response1 = summarize_pdfs_from_folder(txt_input)
            #response = generate_response(txt_input)
            result.append(response1)
            del openai_api_key

if len(result):
    st.info(response1)
