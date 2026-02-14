import io
import pandas as pd
from minio import Minio

# -----------------------------
# MinIO Configuration
# -----------------------------
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

SILVER_BUCKET = "silver"
GOLD_BUCKET = "gold"

# -----------------------------
# Connect to MinIO
# -----------------------------
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# -----------------------------
# Ensure Gold bucket exists
# -----------------------------
if not client.bucket_exists(GOLD_BUCKET):
    client.make_bucket(GOLD_BUCKET)

# -----------------------------
# Get latest silver file
# -----------------------------
objects = list(client.list_objects(SILVER_BUCKET, recursive=True))

if not objects:
    print("❌ No files found in silver bucket!")
    exit()

latest_object = objects[-1].object_name
print(f"📂 Reading from silver file: {latest_object}")

response = client.get_object(SILVER_BUCKET, latest_object)

# ✅ READ AS PARQUET (NOT JSON)
df = pd.read_parquet(io.BytesIO(response.read()))

print("Available columns:", df.columns.tolist())

# -----------------------------
# GOLD TRANSFORMATION
# -----------------------------

# For the dashboard to work as designed (displaying raw data preview and performing its own metrics),
# we need to pass the detailed records.
gold_df = df

# -----------------------------
# Save Gold as PARQUET
# -----------------------------
gold_buffer = io.BytesIO()
gold_df.to_parquet(gold_buffer, index=False)
gold_buffer.seek(0)

client.put_object(
    GOLD_BUCKET,
    "aggregated_data.parquet",
    gold_buffer,
    length=len(gold_buffer.getvalue()),
    content_type="application/octet-stream"
)

print("✅ Gold layer created successfully in MinIO!")
