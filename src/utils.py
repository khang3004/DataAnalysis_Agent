import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def execute_plt_code(code:str, df:pd.DataFrame):
    """ Execute the passing code to plot figure
    Args:
        code (str): The code to execute
        df (pd.DataFrame): The dataframe to use
    Returns:
        plt.gcf(): The figure object
     """
    try:
        local_vars = {"plt": plt, "df": df}
        compiled_code = compile(code, "<string>", "exec")
        exec(compiled_code, globals(), local_vars)

        return plt.gcf()
    except Exception as e:
        st.error(f"ERROR: Can't execute code: {e}")
        return None
    
def execute_code(code:str, df:pd.DataFrame):
    try:
        exec(code)
    except Exception as e:
        st.error(f"ERROR: Can't execute code: {e}")
        return None