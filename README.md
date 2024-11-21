YouTube Data Analyzer
Project Overview
This Streamlit application allows users to  analyze and store data from multiple YouTube channels using Google YouTube Data API and MySQL database.


Features :
  
    1.Retrieve YouTube channel data using Channel ID
    2.Collect data for up to 10 different YouTube channels
    3.Store channel data in a MySQL database
    4.Advanced search and retrieval options
    5.Data visualization and analysis

Prerequisites :
   
    -Python 3.8+
    -Google Cloud Project with YouTube Data API enabled
    -MySQL Database

Now, I'll provide a step-by-step implementation guide for the Streamlit application.

Implementation Steps:

1. Set Up Google Cloud Project
- Go to Google Cloud Console
- Create a new project
- Enable YouTube Data API v3
- Create credentials (API Key)

2. Install Required Libraries
```python
pip install google-api-python-client
pip install streamlit
pip install mysql-connector-python
```

3. YouTube API Interaction
 ```python
from googleapiclient.discovery import build
import os
```

4. Database Operations

   -Create tables to store data from youtube channels

6. Streamlit app
```python
import streamlit as st
```


