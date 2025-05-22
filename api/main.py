from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List, Dict, Any
import uvicorn
from pydantic import BaseModel
import json
from datetime import datetime
import logging

from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from src.models.llms import load_llm
from src.utils import execute_plt_code

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Analysis Agent API",
    description="A comprehensive API for data analysis using AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
MODEL_NAME = 'gemini-2.0-flash'
llm = load_llm(model_name=MODEL_NAME)
current_df = None
da_agent = None

class QueryRequest(BaseModel):
    query: str

class AnalysisResponse(BaseModel):
    output: str
    code: str = None
    plot_data: str = None
    timestamp: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV file for analysis
    """
    global current_df, da_agent
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        # Read the CSV file with low_memory=False to avoid dtype warnings
        df = pd.read_csv(file.file, low_memory=False)
        current_df = df
        
        # Create data analysis agent with handle_parsing_errors=True
        da_agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            agent_type="zero-shot-react-description",
            allow_dangerous_code=True,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True  # Add this parameter
        )
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns)
        }
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_data(request: QueryRequest):
    """
    Analyze data using the uploaded CSV file
    """
    global current_df, da_agent
    
    if current_df is None or da_agent is None:
        raise HTTPException(status_code=400, detail="Please upload a CSV file first")
    
    try:
        response = da_agent.invoke(request.query)
        
        result = {
            "output": response['output'],
            "timestamp": datetime.now().isoformat()
        }
        
        # Check for intermediate steps and code execution
        if response.get('intermediate_steps') and len(response['intermediate_steps']) > 0:
            action = response['intermediate_steps'][-1][0].tool_input.replace('```python\n', '').replace('```', '').replace('`', '')
            
            if action and "plt" in action:
                result["code"] = action
                # Execute plot code and get figure data
                fig = execute_plt_code(action, current_df)
                if fig:
                    # Convert plot to base64 or other suitable format
                    # This is a placeholder - you'll need to implement proper figure serialization
                    result["plot_data"] = "plot_data_here"
        
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/summary")
async def get_data_summary():
    """
    Get summary statistics of the uploaded data
    """
    global current_df
    
    if current_df is None:
        raise HTTPException(status_code=400, detail="Please upload a CSV file first")
    
    try:
        summary = {
            "rows": len(current_df),
            "columns": list(current_df.columns),
            "summary_stats": current_df.describe().to_dict(),
            "missing_values": current_df.isnull().sum().to_dict()
        }
        return summary
    except Exception as e:
        logger.error(f"Error getting data summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "model": MODEL_NAME}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 