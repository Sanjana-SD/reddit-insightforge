import os
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime
from minio import Minio
import os
import shutil


BRONZE_PATH = "data/bronze"
LOCAL_SILVER_PATH = "data/silver_output"


def create_spark():
    return (
        SparkSession.builder
        .appName("Reddit Bronze to Silver")
        .getOrCreate()
    )


def upload_folder_to_minio(local_path, bucket_name):
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)

    for root, dirs, files in os.walk(local_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, local_path)

            client.fput_object(
                bucket_name,
                rel_path.replace("\\", "/"),
                full_path
            )


def main():
    if os.path.exists(LOCAL_SILVER_PATH):
        shutil.rmtree(LOCAL_SILVER_PATH)

    spark = create_spark()

    # Read all subreddit folders together
    df = spark.read.json(f"{BRONZE_PATH}/*/*/*.json")

    # Basic cleaning & normalization
    cleaned = (
        df
        .select(
            col("post_id"),
            col("title"),
            col("author"),
            col("subreddit"),
            col("score"),
            col("num_comments"),
            col("url"),
            col("selftext"),
            from_unixtime(col("created_utc")).alias("created_at")
        )
        .dropna(subset=["post_id", "title", "subreddit"])
        .dropDuplicates(["post_id"])
    )

    cleaned.write.mode("overwrite").parquet(LOCAL_SILVER_PATH)

    spark.stop()

    print("Local silver parquet created.")

    upload_folder_to_minio(
        LOCAL_SILVER_PATH,
        "silver"
    )

    print("Uploaded silver data to MinIO.")


if __name__ == "__main__":
    main()
