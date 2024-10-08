

import streamlit as st
from langchain_OpenAIpy import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.summarize import load_summarize_chain
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
#from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
#import PyPDF2
from langchain import OpenAI, PromptTemplate
import glob
from langchain_anthropic import AnthropicLLM

def summarize_pdfs_from_folder (pdf_file):
    #uploaded_file = st.file_uploader(
    #pdf_file, type="pdf")#, accept_multiple_files=True)
    llm = AnthropicLLM(model='claude-2.1', anthropic_api_key = anthropic_api_key)
    with open(pdf_file.name, mode='wb') as w:
        w.write(pdf_file.getvalue())
    if pdf_file :  # check if path is not None
        loader = PyPDFLoader(pdf_file.name)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run(docs)
        return summary

def summarize_pdfs_from_folder1 (pdf_file):
    #uploaded_file = st.file_uploader(
    #pdf_file, type="pdf")#, accept_multiple_files=True)
    llm = OpenAI(model_name='davinci-002',  openai_api_key=openai_api_key)
    with open(pdf_file.name, mode='wb') as w:
        w.write(pdf_file.getvalue())
    if pdf_file :  # check if path is not None
        loader = PyPDFLoader(pdf_file.name)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run(docs)
        return summary



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
CUSTOM_PROMPT = "Write a concise summary of the following paper with this structure: Problem being solved; Approach; Main results; Main Discussion Points"
custom_summaries = custom_summary("./pdfs", custom_prompt=CUSTOM_PROMPT)
# Save all summaries into one .txt file
with open("custom_summaries.txt", "w") as f:
    for summary in custom_summaries:
        f.write(summary + "\n"*3)
def generate_response1(txt):
    # Instantiate the LLM model
    llm = OpenAI(temperature=0.2, openai_api_key=openai_api_key)
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

#txt_input = st.text_area('upload your pdf file', '', height=200)

uploaded_file = st.file_uploader(
    "upload pdf file", type="pdf")#, accept_multiple_files=True)
#for uploaded_file in uploaded_files:
#if uploaded_file is not None:
    # Read the PDF file
 #   pdf_reader = PyPDF2.PdfReader(uploaded_file)
    # Extract the content
 #   content = ""
 #   for page in range(len(pdf_reader.pages)):
 #       content += pdf_reader.pages[page].extract_text()
    # Display the content
 #   st.write(content)

# Form to accept user's text input for summarization

result = []
with st.form('summarize_form', clear_on_submit=True):
    anthropic_api_key = st.text_input('ANTHROPIC API KEY', type='password')
    submitted = st.form_submit_button('Submit')
    if submitted and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response= summarize_pdfs_from_folder(uploaded_file)
            #response = generate_response(txt_input )
            result.append(response)
            del anthropic_api_key
if len(result):
    st.info(response)

result1 = []
with st.form('summarize_form1', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type = 'password')
    submitted = st.form_submit_button('Submit')
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response1= summarize_pdfs_from_folder1(uploaded_file)
            #response = generate_response(txt_input )
            result1.append(response1)
            del openai_api_key


if len(result1):
    st.info(response1)