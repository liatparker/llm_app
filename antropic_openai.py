import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
import tiktoken
from tqdm import tqdm
from anthropic import Anthropic
import pandas as pd


# reader = PdfReader("/Users/Liatparker/downloads/attention_is_all_you_need.pdf")
# number_of_pages = len(reader.pages)
# text = ''.join(page.extract_text() for page in reader.pages)
#

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



# Page title
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

# Text input

#txt_input = st.text_area('upload your pdf file', '', height=200)

uploaded_file = st.file_uploader(
    "upload pdf file", type="pdf")#, accept_multiple_files=True)


if uploaded_file:  # check if path is not None
    reader = PdfReader(uploaded_file)
    text = ''.join(page.extract_text() for page in reader.pages)

#MODEL_NAME = "claude-3-opus-20240229"

MODEL_NAME = 'claude-3-5-sonnet-20240620'
result = []
with st.form('summarize_form', clear_on_submit=False):
    anthropic_api_key = st.text_input('ANTHROPIC API KEY', type='password')
    submitted = st.form_submit_button('Submit')
    if submitted and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
             response = get_completion(client = Anthropic(api_key=anthropic_api_key)  ,prompt= (
                                         f"""Here is an academic paper: <paper>{text}</paper>
                                           Please do the following:
                                           1.Write in bullet point form and focus on hypothesis, methodology, results, and conclusions (<extract summary>)
                                           """
                                           #2. Write in bullet point form and focus on major sections (<extract summary2>)"""


                                        ))

             result.append(response)
             del anthropic_api_key
if len(result):
    st.info(response)

result1 = []

txt_input = st.text_input('please write your own critiria for a summary', '', height=200)
submitted1 = st.form_submit_button('Submit')
if submitted1 and anthropic_api_key.startswith('sk-'):
    with st.spinner('Calculating...'):
        response1 = get_completion(client = Anthropic(api_key=anthropic_api_key)  ,prompt= (
                                         f"""Here is an academic paper: <paper>{text}</paper>
                                           Please do the following:{txt_input}
                                           
                                           """
                                           #2. Write in bullet point form and focus on major sections (<extract summary2>)"""


                                        ))

        result1.append(response1)
        del anthropic_api_key
if len(result1):
    st.info(response1)

