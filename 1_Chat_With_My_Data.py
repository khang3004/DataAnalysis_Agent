import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI


from src.logger.base import BaseLogger
from src.models.llms import load_llm
from src.utils import execute_plt_code
#load enviroment variables
load_dotenv()
logger = BaseLogger()
MODEL_NAME = 'gemini-2.0-flash'

def process_query(da_agent, query):
    try:
        response = da_agent.invoke(query)
        
        if response.get('intermediate_steps') and len(response['intermediate_steps']) > 0 and len(response['intermediate_steps'][-1]) > 0:
            action = response['intermediate_steps'][-1][0].tool_input.replace('```python\n', '').replace('```', '').replace('`', '')
        else:
            action = None
        
        if action is not None and "plt" in action:
            st.write(response['output'])
            fig = execute_plt_code(action, st.session_state.df)
            if fig:
                st.pyplot(fig)
            
            st.write("**Executed code:**")
            st.code(action)
            
            string_to_display = response['output'] + "\n" + f'python\n{action}\n'
            st.session_state.history.append((query, string_to_display)) 
            
        else:
            st.write(response['output'])
            st.session_state.history.append((query, response['output'])) 
        
        # # Kiểm tra và xử lý intermediate steps nếu có
        # if response.get('intermediate_steps') and len(response['intermediate_steps']) > 0:
        #     last_step = response['intermediate_steps'][-1]
        #     if last_step and len(last_step) > 0:
        #         action = last_step[0].tool_input.replace('```python\n', '').replace('```', '')
        #         st.code(action, language='python')
        
        # # Hiển thị kết quả cuối cùng
        # if response.get('output'):
        #     st.write(response['output'])
        # else:
        #     st.write("No output available")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    #Display the chat history

def display_chat_history():
    st.markdown("### Chat History")
    for i, (q,r) in enumerate(st.session_state.history):
        st.markdown(f"**Question {i+1}:** {q}")
        st.markdown(f"**Answer {i+1}:** {r}")
        st.markdown("-------------------------")

def main():
    #Set up the streamlit interface
    st.set_page_config(
        page_title="SMART DATA ANALYSIS TOOL",
        page_icon=":bar_chart:",
        layout="centered",
    )
    st.header("SMART DATA ANALYSIS TOOL")
    st.write("### WELCOME TO OUR SMART DATA ANALYSIS TOOL. THIS TOOL IS DESIGNED TO HELP YOU ANALYZE YOUR DATA AND GET INSIGHTS FROM IT. PLS ENJOY!###")
    
    #Load LLM model
    llm = load_llm(model_name=MODEL_NAME)
    logger.info(f"-----Successfully Loaded LLM model: {MODEL_NAME}!-----")
    
    #Upload csv file
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        
        
    #Initialize the chat history
    if "history" not in st.session_state:
        st.session_state.history = [
            
        ]
    #Read csv file
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write("### Your uploaded file has been loaded successfully!",st.session_state.df.head())
        
        #Create data analysis agent to query with our data
        da_agent = create_pandas_dataframe_agent(
            llm=llm, 
            df=st.session_state.df,
            agent_type="zero-shot-react-description",
            allow_dangerous_code=True,
            verbose=True,
            return_intermediate_steps=True)
        
        logger.info(f"-----Successfully Created Data Analysis Agent!-----")
    
        #Display the agent
        st.write("### Your data analysis agent has been created successfully!",da_agent)
        
        #Input query and process query
        query = st.text_input("### Enter your question here: ###")
        if st.button("### Run Query"):
            with st.spinner("Processing your query..."):
                process_query(da_agent, query)
        #Display the results
    st.divider()
    display_chat_history()

if __name__ == "__main__":
    main()







