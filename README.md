# Data Analysis Agent API

A powerful FastAPI-based REST API for data analysis using AI agents. This 	API allows you to upload CSV files, perform data analysis, and get insights using natural language queries.

## 
    Features

- Upload and process CSV files
- Natural language data analysis queries
- Automatic visualization generation
- Data summary statistics
- Health check endpoint
- CORS support
- Comprehensive error handling

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

## Running the API

Start the server with:

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### 1. Upload CSV File

- **POST** `/upload`
- Upload a CSV file for analysis
- Returns file information and basic statistics

#### 2. Analyze Data

- **POST** `/analyze`
- Send natural language queries about your data
- Returns analysis results, code, and visualizations

#### 3. Get Data Summary

- **GET** `/data/summary`
- Get comprehensive statistics about the uploaded data
- Returns row count, columns, summary statistics, and missing values

#### 4. Health Check

- **GET** `/health`
- Check API health status
- Returns current model information

## Example Usage

### Upload a CSV file

```python
import requests

files = {'file': open('your_data.csv', 'rb')}
response = requests.post('http://localhost:8000/upload', files=files)
print(response.json())
```

### Analyze data

```python
query = {
    "query": "What is the correlation between column A and column B?"
}
response = requests.post('http://localhost:8000/analyze', json=query)
print(response.json())
```

### Get data summary

```python
response = requests.get('http://localhost:8000/data/summary')
print(response.json())
```

## Error Handling

The API includes comprehensive error handling for:

- Invalid file types
- Missing files
- Analysis errors
- Server errors

All errors return appropriate HTTP status codes and detailed error messages.

## Security

- CORS middleware is enabled for cross-origin requests
- File type validation for uploads
- Environment variable management for sensitive data

## Contributing

Feel free to submit issues and enhancement requests!
