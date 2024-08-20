import streamlit as st
from pypdf import PdfReader
import os
from openai import OpenAI
import tiktoken
from tqdm import tqdm
from anthropic import Anthropic

import pandas as pd


# reader = PdfReader("/Users/Liatparker/downloads/attention_is_all_you_need.pdf")
# number_of_pages = len(reader.pages)
# text = ''.join(page.extract_text() for page in reader.pages)
#anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
#os.environ['ANTHROPIC_API_KEY'] = anthropic_api_key
#client = Anthropic(api_key= anthropic_api_key)
#os.environ.get('ANTHROPIC_API_KEY', anthropic_api_key)
#MODEL_NAME = "claude-3-opus-20240229"
#MODEL_NAME = 'claude-3-5-sonnet-20240620'



# Page title
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

uploaded_file = st.file_uploader(
    "upload pdf file", type="pdf")


def create_messages(prompts):

    summaries= []

    for prompt in prompts :
        message = {"role": 'user', "content": prompt
             }
        summaries.append(message)
    return summaries
def get_completion(client, prompts):


    client = Anthropic(api_key=anthropic_api_key)
    MODEL_NAME = 'claude-3-5-sonnet-20240620'
    return client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        messages= create_messages(prompts)
    ).content[0].text




# Text input

#txt_input = st.text_area('upload your pdf file', '', height=200)

# uploaded_file = st.file_uploader(
#     "upload pdf file", type="pdf")#, accept_multiple_files=True)





# if uploaded_file is not None:
#     text = ""
#     reader = PdfReader(uploaded_file)
#     for page in reader.pages:
#         text += page.extract_text()




client = Anthropic()
#MODEL_NAME = "claude-3-opus-20240229"
MODEL_NAME = 'claude-3-5-sonnet-20240620'
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    text = ''.join(page.extract_text() for page in reader.pages)
prompt1 = f"""Here is an academic paper: <paper>{text}</paper>

                       Please do the following:

                       Write in bullet point form and focus on hypothesis, methodology, results, and conclusions (<extract summary>)"""

prompt2 = f"""Here is an academic paper: <paper>{text}</paper>

                                    Please do the following:

                                    Write in bullet point form and focus on major sections (<extract summary>)"""









result = []
with st.form('summarize_form', clear_on_submit=True):
    anthropic_api_key = st.text_input('ANTHROPIC API KEY', type='password')
    txt_input1 = st.text_area('summary focused on hypothesis, methodology, results and conclusions', '', height=200)
    submitted1 = st.form_submit_button('submit')
    txt_input2 = st.text_area('summary focused on major sections ', '', height=200)
    submitted2 = st.form_submit_button('Submit')

    if submitted1 and anthropic_api_key.startswith('sk-') :
        with st.spinner('Calculating...'):
                response = get_completion(client, prompt1)
                result.append(response)
                del anthropic_api_key
    if submitted2 and anthropic_api_key.startswith('sk-') :
        with st.spinner('Calculating...'):
                response = get_completion(client, prompt2)
                result.append(response)
                del anthropic_api_key





if len(result):
    st.info(result)

# result1 = []
# with st.form('summarize_form1', clear_on_submit=True):
#     openai_api_key = st.text_input('OpenAI API Key', type = 'password')
#     submitted = st.form_submit_button('Submit')
#     if submitted and openai_api_key.startswith('sk-'):
#         with st.spinner('Calculating...'):
#             response1= summarize_pdfs_from_folder1(uploaded_file)
#             #response = generate_response(txt_input )
#             result1.append(response1)
#             del openai_api_key
#
#
# if len(result1):
#     st.info(response1)