import json
from minio import Minio
from io import BytesIO
import pandas as pd

# -----------------------------
# MinIO Configuration
# -----------------------------
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bronze_bucket = "bronze"
silver_bucket = "silver"

# 👇 IMPORTANT: Match your actual object path from MinIO
bronze_object = "bronze/programming/2026-02-12/reddit_133744.json"


# -----------------------------
# Step 1: Get Data from Bronze
# -----------------------------
response = client.get_object(bronze_bucket, bronze_object)
data = json.loads(response.read())


# -----------------------------
# Step 2: Convert to DataFrame
# -----------------------------
df = pd.DataFrame(data)


# -----------------------------
# Step 3: Basic Cleaning
# -----------------------------
df = df.drop_duplicates()
df = df.dropna()

# Example: Keep only important columns (edit if needed)
columns_to_keep = [col for col in df.columns if col in ["id", "title", "author", "score", "created_utc", "subreddit"]]
if columns_to_keep:
    df = df[columns_to_keep]


# -----------------------------
# Step 4: Convert to Parquet
# -----------------------------
parquet_buffer = BytesIO()
df.to_parquet(parquet_buffer, index=False)
parquet_buffer.seek(0)


# -----------------------------
# Step 5: Upload to Silver
# -----------------------------
if not client.bucket_exists(silver_bucket):
    client.make_bucket(silver_bucket)

client.put_object(
    silver_bucket,
    "reddit_cleaned.parquet",
    parquet_buffer,
    length=parquet_buffer.getbuffer().nbytes,
    content_type="application/octet-stream"
)

print("✅ Silver layer created successfully in MinIO!")
