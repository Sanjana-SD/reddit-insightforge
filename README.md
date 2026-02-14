# Reddit Insight Intelligence Platform

Real-time Subreddit Analytics powered by a Scalable Data Engineering Pipeline with a startup-grade Streamlit Dashboard.

## 🚀 Features
- **Glassmorphism UI**: Modern aesthetic with animated KPI cards.
- **Interactive Charts**: Advanced Plotly visualizations for deep analysis.
- **Modular Data Engineering**: Robust data loading from MinIO with caching.
- **Automated Insights**: Intelligence panel for quick takeaways.
- **Cloud Ready**: Automatic fallback to static data when deployed to Streamlit Community Cloud.

## 🛠️ Tech Stack
- **Frontend**: Streamlit, Plotly, CSS3 (Glassmorphism)
- **Data Engineering**: MinIO (S3 compatible object storage), Pandas, PyArrow
- **Deployment**: Streamlit Community Cloud

## 📦 Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/reddit-insightforge.git
    cd reddit-insightforge
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start Infrastructure (Optional)**:
    If you want live data ingestion, start MinIO and Airflow services (docker-compose required):
    ```bash
    docker-compose up -d
    ```

4.  **Run Dashboard**:
    ```bash
    streamlit run dashboard/app.py
    ```

## ☁️ Deployment (Streamlit Community Cloud)

This project is configured to deploy instantly on [Streamlit Community Cloud](https://streamlit.io/cloud).

1.  Push this code to a GitHub repository.
2.  Go to Streamlit Community Cloud and connect your repository.
3.  Set the **Main file path** to: `dashboard/app.py`
4.  And click **Deploy**!

**Note**: When deployed, the app will automatically detect it cannot reach the local MinIO instance and will switch to **Offline Mode**, serving sample data from `dashboard/data/sample_data.parquet`.
