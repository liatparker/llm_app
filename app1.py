

import streamlit as st
from langchain_openai import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.summarize import load_summarize_chain
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
#from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
#import PyPDF2
#from langchain import OpenAI, PromptTemplate
import glob
from langchain_anthropic import AnthropicLLM

def summarize_pdfs_from_folder (pdf_file):
    #uploaded_file = st.file_uploader(
    #pdf_file, type="pdf")#, accept_multiple_files=True)
    llm1 = OpenAI(temperature=0.2,model_name='gpt-4-turbo', openai_api_key=openai_api_key)
    llm = AnthropicLLM(model='claude-2.1', anthropic_api_key = anthropic_api_key)

    with open(pdf_file.name, mode='wb') as w:
        w.write(pdf_file.getvalue())
    #summaries = []
    #for pdf_file in pdfs_folder:
    #for pdf_file in glob.glob(pdfs_folder + "/*.pdf"):
    #pdf_file = glob.glob(pdf_file)
    if pdf_file :  # check if path is not None
        loader = PyPDFLoader(pdf_file.name)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="stuff")
        chain1 = load_summarize_chain(llm1, chain_type="stuff")
        summary = chain.run(docs)
        summary1 = chain1.run(docs)
        return summary, summary1
       #st.write(summary)
    #print("Summary for: ", pdf_file)
    #print(summary)
        #print("\n")
        #summaries.append(summary)
    #return summary
    #return summaries


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

def generate_response1(txt):
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
            response= summarize_pdfs_from_folder(uploaded_file)[0]
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
            response1= summarize_pdfs_from_folder(uploaded_file)[1]
            #response = generate_response(txt_input )
            result1.append(response1)
            del openai_api_key


if len(result1):
    st.info(response1)