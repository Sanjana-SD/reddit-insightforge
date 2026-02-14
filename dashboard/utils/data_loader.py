import streamlit as st
import pandas as pd
from minio import Minio
from io import BytesIO

# MinIO Config
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "gold"
OBJECT_NAME = "aggregated_data.parquet"

@st.cache_data(ttl=60) # Cache for 60 seconds
def load_data():
    """
    Loads Parquet data from MinIO with caching.
    """
    try:
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )
        
        # Check if bucket exists
        if not client.bucket_exists(BUCKET_NAME):
            st.error(f"Bucket '{BUCKET_NAME}' does not exist.")
            return pd.DataFrame()

        response = client.get_object(BUCKET_NAME, OBJECT_NAME)
        data = BytesIO(response.read())
        df = pd.read_parquet(data)
        
        # Ensure datetime conversion
        if 'created_utc' in df.columns:
            df['created_utc'] = pd.to_datetime(df['created_utc'])
            
        return df

    except Exception as e:
        # Fallback for Streamlit Cloud or offline mode
        try:
            return pd.read_parquet("dashboard/data/sample_data.parquet")
        except FileNotFoundError:
            st.error("MinIO is unreachable and no offline data found.")
            return pd.DataFrame()
