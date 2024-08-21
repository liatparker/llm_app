import streamlit as st
from pypdf import PdfReader
import PyPDF2
from openai import OpenAI
import tiktoken
from tqdm import tqdm
from anthropic import Anthropic
from transformers import GPT2TokenizerFast
import pandas as pd


# reader = PdfReader("/Users/Liatparker/downloads/attention_is_all_you_need.pdf")
# number_of_pages = len(reader.pages)
# text = ''.join(page.extract_text() for page in reader.pages)
#
client = Anthropic()
#MODEL_NAME = "claude-3-opus-20240229"
MODEL_NAME = 'claude-3-5-sonnet-20240620'


def get_completion(client, prompt):
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


# Form to accept user's text input for summarization



if uploaded_file:  # check if path is not None
    reader = PdfReader(uploaded_file)
    text = ''.join(page.extract_text() for page in reader.pages)





#MODEL_NAME = "claude-3-opus-20240229"
MODEL_NAME = 'claude-3-5-sonnet-20240620'
result = []
with st.form('summarize_form', clear_on_submit=True):
    anthropic_api_key = st.text_input('ANTHROPIC API KEY', type='password')
    submitted = st.form_submit_button('Submit')
    if submitted and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
             response = get_completion(client = Anthropic(),prompt= (
                                         f"""Here is an academic paper: <paper>{text}</paper>
                                           Please do the following:
                                           Write in point form and focus on hypothesis, methodology, results, and conclusions (<extract summary>)""",
                                         f"""Here is an academic paper: <paper>{text}</paper>
                                                        Please do the following:
                                                        Write in point form and focus on major sections (<extract summary>)"""


                                        ))

             result.append(response)
             del anthropic_api_key
if len(result):
    st.info(response)

