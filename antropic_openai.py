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


def get_completion(client, prompt):
    client = Anthropic(api_key=anthropic_api_key)
    MODEL_NAME = 'claude-3-5-sonnet-20240620'
    return client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
    messages=[{
            "role": 'user', "content":  prompt
        }]
    ).content[0].text

# completion1 = get_completion(client,
#     f"""Here is an academic paper: <paper>{text}</paper>
#
# Please do the following:
#
#  Write in point form and focus on hypothesis, methodology, results, and conclusions (<extract summary>)
#
# """
# )
#
# completion2 = get_completion(client,
#     f"""Here is an academic paper: <paper>{text}</paper>
#
# Please do the following:
#
#  Write summary in bullets form  focus on subtitles (<extract summary>)
#
#
# """
# )
# print(completion1,completion2)


# Page title
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

# Text input

#txt_input = st.text_area('upload your pdf file', '', height=200)

uploaded_file = st.file_uploader(
    "upload pdf file", type="pdf")#, accept_multiple_files=True)

import streamlit as st



if uploaded_file is not None:
    text = ""
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()




client = Anthropic()
#MODEL_NAME = "claude-3-opus-20240229"
MODEL_NAME = 'claude-3-5-sonnet-20240620'
result = []
with st.form('summarize_form', clear_on_submit=True):
    anthropic_api_key = st.text_input('ANTHROPIC API KEY', type='password')
    submitted = st.form_submit_button('Submit')
    if submitted and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            prompts = [
                                         f"""Here is an academic paper: <paper>{text}</paper>

                                           Please do the following:

                                           Write in point form and focus on hypothesis, methodology, results, and conclusions (<extract summary>)""",
                                         f"""Here is an academic paper: <paper>{text}</paper>

                                                        Please do the following:

                                                        Write in point form and focus on major sections (<extract summary>)"""


                                        ]
            for prompt in prompts:
                response = get_completion(client, prompt= prompt)

                result.append(response)
            del anthropic_api_key
if len(result):
    st.info(response)

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