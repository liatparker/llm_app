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
st.set_page_config(page_title=' Pdf paper Summarization/chat App')
st.title(' Pdf paper App')

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
    txt_input = st.text_input("summary focused on hypothesis, methodology, results, and conclusions")
    submitted = st.form_submit_button('Submit')
    if submitted and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
             response = get_completion(client = Anthropic(api_key=anthropic_api_key)  ,prompt= (
                                         f"""Here is an academic paper: <paper>{text}</paper>
                                           Please do the following:
                                           1.Write in bullet point form and focus on hypothesis, methodology, results, and conclusions 
                                           """
                                           #2. Write in bullet point form and focus on major sections (<extract summary2>)"""


                                        ))

             result.append(response)
             del anthropic_api_key
if len(result):
    st.info(response)

result0 = []
with st.form('summarize_form0', clear_on_submit=False):
    txt_input = st.text_input("summary focused on major sections")
    submitted0 = st.form_submit_button('Submit')
    if submitted0 and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response0 = get_completion(client=Anthropic(api_key=anthropic_api_key), prompt=(
                f"""Here is an academic paper: <paper>{text}</paper>
                                            Please do the following:
                                            Write in bullet point form and focus on major sections  
                                            """
            ))

            result0.append(response0)
            del anthropic_api_key
if len(result0):
    st.info(response0)

result1 = []
with st.form('summarize_form1', clear_on_submit=False):
    txt_input = st.text_input("summary focused on architecture of the model ")
    submitted1 = st.form_submit_button('Submit')
    if submitted1 and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response1 = get_completion(client=Anthropic(api_key=anthropic_api_key), prompt=(
                f"""Here is an academic paper: <paper>{text}</paper>
                                            Please do the following:
                                            
                                             what is the architecture of the model 
                                            """
            ))

            result1.append(response1)
            del anthropic_api_key
if len(result1):
    st.info(response1)

result2 = []
with st.form('summarize_form2', clear_on_submit=False):
    txt_input = st.text_input('please write your own critiria for a summary or ask anything about the paper you uploaded', key="widget")
    submitted2 = st.form_submit_button('Submit')
    if submitted2 and anthropic_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response2 = get_completion(client=Anthropic(api_key=anthropic_api_key), prompt=(
                f"""Here is an academic paper: <paper>{text}</paper>
                                            Please do the following:{txt_input}

                                            """


            ))

            result2.append(response2)
            del anthropic_api_key
if len(result2):
    st.info(response2)

