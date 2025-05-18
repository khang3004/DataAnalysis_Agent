import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

def main():
    # set up the streamlit interface
    st.set_page_config(
        page_title="🤣🤣🤣Interactive Visualization Tools", 
        page_icon=":bar_chart:", 
        layout="wide"
        )
    st.title("🤣🤣🤣Interactive Visualization Tools")
    st.header("🤣🤣🤣Interactive Visualization Tools")
    st.write("##Welcome to the INTERACTIVE VISUALIZATION TOOL. PLS ENJOY!")

    
    
    #Load data
        
    #Render pygwalker
    if st.session_state.get("df") is not None and not st.session_state.df.empty:
        pyg_app = StreamlitRenderer(st.session_state.df)
        pyg_app.explorer()
    elif st.session_state.get("df") is not None and st.session_state.df.empty:
        st.warning("The uploaded dataset is empty. Please upload a valid CSV file with data.")
    else:
        st.info("Please upload a dataset to begin using the interactive visualization tools!")
        


    
if __name__ == "__main__":
    main()