import json
import datetime
from minio import Minio
import io

# MinIO Configuration
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "bronze"
object_name = "bronze/programming/2026-02-12/reddit_133744.json"

# Create Data
data = [
    {
        "id": "1",
        "title": "Python is great",
        "author": "dev_user",
        "score": 100,
        "created_utc": 1676200000,
        "subreddit": "programming"
    },
    {
        "id": "2",
        "title": "Rust vs C++",
        "author": "rust_fan",
        "score": 250,
        "created_utc": 1676200100,
        "subreddit": "programming"
    },
    {
        "id": "3",
        "title": "Kubernetes tips",
        "author": "k8s_guru",
        "score": 150,
        "created_utc": 1676200200,
        "subreddit": "devops"
    }
]

# Ensure bucket exists
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Upload Data
json_data = json.dumps(data).encode('utf-8')
client.put_object(
    bucket_name,
    object_name,
    io.BytesIO(json_data),
    length=len(json_data),
    content_type="application/json"
)

print(f"✅ Uploaded sample data to {bucket_name}/{object_name}")
