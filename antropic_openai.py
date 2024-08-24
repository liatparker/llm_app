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
        temperature=0.0,
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

# result0 = []
# with st.form('summarize_form0', clear_on_submit=False):
#     txt_input = st.text_input("summary focused on major sections")
#     submitted0 = st.form_submit_button('Submit', clear_on_submit=False)
#     if submitted0 and anthropic_api_key.startswith('sk-'):
#         with st.spinner('Calculating...'):
#             response0 = get_completion(client=Anthropic(api_key=anthropic_api_key), prompt=(
#                 f"""Here is an academic paper: <paper>{text}</paper>
#                                             Please do the following:
#                                             Write in bullet point form and focus on major sections
#                                             """
#             ))
#
#             result0.append(response0)
#             del anthropic_api_key
# if len(result0):
#     st.info(response0)

# result1 = []
# with st.form('summarize_form1', clear_on_submit=False):
#     txt_input = st.text_input("summary focused on architecture of the model ")
#     submitted1 = st.form_submit_button('Submit', clear_on_submit=False)
#     if submitted1 and anthropic_api_key.startswith('sk-'):
#         with st.spinner('Calculating...'):
#             response1 = get_completion(client=Anthropic(api_key=anthropic_api_key), prompt=(
#                 f"""Here is an academic paper: <paper>{text}</paper>
#                                             Please do the following:
#
#                                              what is the architecture of the model
#                                             """
#             ))
#
#             result1.append(response1)
#             del anthropic_api_key
# if len(result1):
#     st.info(response1)
#
# result2 = []
# with st.form('summarize_form2',clear_on_submit=False):
#     txt_input = st.text_input('please write your own critiria for a summary or ask anything about the paper you uploaded', key="widget")
#     submitted2 = st.form_submit_button('Submit', clear_on_submit=False )
#     if submitted2 and anthropic_api_key.startswith('sk-'):
#         with st.spinner('Calculating...'):
#             response2 = get_completion(client=Anthropic(api_key=anthropic_api_key), prompt=(
#                 f"""Here is an academic paper: <paper>{text}</paper>
#                                             Please do the following:{txt_input}
#
#                                             """
#
#
#             ))
#
#             result2.append(response2)
#             del anthropic_api_key
# if len(result2):
#     st.info(response2)


# Evaluation prompt template based on G-Eval
EVALUATION_PROMPT_TEMPLATE = """                                                                                                                              
You will be given one summary written for an article. Your task is to rate the summary on one metric.                                                         
Please make sure you read and understand these instructions very carefully.                                                                                   
Please keep this document open while reviewing, and refer to it as needed.                                                                                    

Evaluation Criteria:                                                                                                                                          

{criteria}                                                                                                                                                    

Evaluation Steps:                                                                                                                                             

{steps}                                                                                                                                                       

Example:                                                                                                                                                      

Source Text:                                                                                                                                                  

{document}                                                                                                                                                    

Summary:                                                                                                                                                      

{summary}                                                                                                                                                     

Evaluation Form (scores ONLY):                                                                                                                                

- {metric_name}                                                                                                                                               
"""

# Metric 1: Relevance

RELEVANCY_SCORE_CRITERIA = """                                                                                                                                
(1-5) - selection of important content from the source. \                                                                                                     
The summary should include only important information from the source document. \                                                                             
Annotators were instructed to penalize summaries which contained redundancies and excess information.                                                         
"""

RELEVANCY_SCORE_STEPS = """                                                                                                                                   
1. Read the summary and the source document carefully.                                                                                                        
2. Compare the summary to the source document and identify the main points of the article.                                                                    
3. Assess how well the summary covers the main points of the article, and how much irrelevant or redundant information it contains.                           
4. Assign a relevance score from 1 to 5.                                                                                                                      
"""

# Metric 2: Coherence

COHERENCE_SCORE_CRITERIA = """                                                                                                                                
(1-5) - the collective quality of all sentences. \                                                                                                            
We align this dimension with the DUC quality question of structure and coherence \                                                                            
whereby "the summary should be well-structured and well-organized. \                                                                                          
The summary should not just be a heap of related information, but should build from sentence to a\                                                            
coherent body of information about a topic."                                                                                                                  
"""

COHERENCE_SCORE_STEPS = """                                                                                                                                   
1. Read the article carefully and identify the main topic and key points.                                                                                     
2. Read the summary and compare it to the article. Check if the summary covers the main topic and key points of the article,                                  
and if it presents them in a clear and logical order.                                                                                                         
3. Assign a score for coherence on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.                            
"""

# Metric 3: Consistency

CONSISTENCY_SCORE_CRITERIA = """                                                                                                                              
(1-5) - the factual alignment between the summary and the summarized source. \                                                                                
A factually consistent summary contains only statements that are entailed by the source document. \                                                           
Annotators were also asked to penalize summaries that contained hallucinated facts.                                                                           
"""

CONSISTENCY_SCORE_STEPS = """                                                                                                                                 
1. Read the article carefully and identify the main facts and details it presents.                                                                            
2. Read the summary and compare it to the article. Check if the summary contains any factual errors that are not supported by the article.                    
3. Assign a score for consistency based on the Evaluation Criteria.                                                                                           
"""

# Metric 4: Fluency

FLUENCY_SCORE_CRITERIA = """                                                                                                                                  
(1-5): the quality of the summary in terms of grammar, spelling, punctuation, word choice, and sentence structure.                                     
1: The summary has many errors that make it hard to understand or sound unnatural.                                                                                           
5: The summary has few or no errors and is easy to read and follow.                                                                                     
"""

FLUENCY_SCORE_STEPS = """                                                                                                                                     
Read the summary and evaluate its fluency based on the given criteria. Assign a fluency score from 1 to 5.                                                    
"""


def get_geval_score(

        criteria: str, steps: str, summary: str, metric_name: str, client, document: str
):
    prompt = EVALUATION_PROMPT_TEMPLATE.format(
        criteria=criteria,
        steps=steps,
        metric_name=metric_name,
        document=document,
        summary=summary,
    )
    response = client.chat.completions.create(
        model='gpt-4-turbo',
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content


evaluation_metrics = {
    "Relevance": (RELEVANCY_SCORE_CRITERIA, RELEVANCY_SCORE_STEPS),
    "Coherence": (COHERENCE_SCORE_CRITERIA, COHERENCE_SCORE_STEPS),
    "Consistency": (CONSISTENCY_SCORE_CRITERIA, CONSISTENCY_SCORE_STEPS),
    "Fluency": (FLUENCY_SCORE_CRITERIA, FLUENCY_SCORE_STEPS),
}



# summary = st.text_area( label =' please enter the summary for evaluation' )
# summary_result = {"Summary 1": summary }
# data = {"Evaluation Type": [], "Summary Type": [], "Score": []}
# for eval_type, (criteria, steps) in evaluation_metrics.items():
#     for summ_type, summary in summary_result.items():
#         data["Evaluation Type"].append(eval_type)
#         data["Summary Type"].append(summ_type)
#         result = get_geval_score(criteria, steps, summary, eval_type, text)
#         score_num = int(result.strip())
#         data["Score"].append(score_num)
#
#         pivot_df = pd.DataFrame(data, index=None).pivot(
#         index="Evaluation Type", columns="Summary Type", values="Score"
#         )
#styled_pivot_df = pivot_df.style.highlight_max



with st.form('summarize_form3',clear_on_submit=False):
    openai_api_key = st.text_input('OpenAI API Key', type='password')
    summary = st.text_area(label=' please enter the summary for evaluation')
    submitted3 = st.form_submit_button('Submit')
    if submitted3 and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):


            summary_result = {"Summary 1": summary}
            data = {"Evaluation Type": [], "Summary Type": [], "Score": []}
            for eval_type, (criteria, steps) in evaluation_metrics.items():
                for summ_type, summary in summary_result.items():
                    data["Evaluation Type"].append(eval_type)
                    data["Summary Type"].append(summ_type)
                    response3 = get_geval_score(criteria, steps, summary, eval_type,client = OpenAI(api_key= openai_api_key), text = text )
                    score_num = int(response3.strip())
                    data["Score"].append(score_num)
                    pivot_df = pd.DataFrame(data, index=None).pivot(index="Evaluation Type", columns="Summary Type", values="Score")




if len(pivot_df):
    st.info(pivot_df)



