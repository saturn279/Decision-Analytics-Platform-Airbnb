# Decision Analytics Platform for Airbnb Data

Welcome to the **Decision Analytics Platform for Airbnb**, a powerful batch processing and analytics framework designed to help you gain insights and make informed decisions using Airbnb data. Whether you're a host, traveler, or simply interested in Airbnb trends, our platform provides you with comprehensive tools for analysis, visualization, and prediction. This document will guide you through the installation process and demonstrate how to use the platform effectively.

## Demo
Check out our [Client Interface Demo](https://user-images.githubusercontent.com/101204171/206233456-49c86b3e-62a8-4cfa-9496-409603191465.webm) to get a glimpse of the platform's features.

[VIdeo](https://user-images.githubusercontent.com/101204171/206233456-49c86b3e-62a8-4cfa-9496-409603191465.webm)

## Quickstart with Docker
Experience the power of our platform in minutes using Docker.

1. Run the following command to launch the platform:
    ```bash
    docker run -p 8501:8501 -p 8502:8502 sk1297/decision-analytics-prod
    ```

2. Access the client interface by navigating to [http://localhost:8502](http://localhost:8502), where you can select your desired city and build a customized pipeline.

3. Explore visualizations and analysis at [http://localhost:8501](http://localhost:8501), where you can leverage built-in machine learning models to make predictions based on your selected city.

## Installation Options
Choose the installation method that best fits your needs.

### Pre-deployed Version (Streamlit Cloud)
Access the platform instantly without any installation by visiting our [Streamlit Cloud deployment](https://saturn279-deploy-airbnb-streamlit-app-4za9hw.streamlitapp.com).

### Portable Installation
Follow these steps for a portable installation on your local machine:

**Prerequisites:**
Ensure you have the required packages installed by running:
```bash
pip install scikit-learn bs4 xgboost pandas requests numpy matplotlib streamlit 
```

**Installation:**
1. Clone the repository and navigate to the deployment directory:
    ```bash
    git clone https://github.com/saturn279/Decision-Analytics-Platform-Airbnb
    cd Decision-Analytics-Platform-Airbnb/Code/Deployment
    ```

2. Run the internal streamlit app:
    ```bash
    streamlit run streamlit_internal.py
    ```

3. In a new terminal, run the main streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```

### Hadoop Cluster Setup
For more advanced users, you can integrate the platform with a Hadoop cluster for enhanced performance and scalability. Here's how:

1. Ensure you have Python 3.7+ and Hadoop 3+ installed.

2. Start the Hadoop Distributed File System (HDFS):
    ```bash
    bash run-hdfs.sh -s start
    ```

### Apache Airflow Integration
For seamless workflow automation, consider integrating the platform with Apache Airflow:

1. Install Python 3.7+ and Apache Airflow 1.10+.

2. Start the Airflow components (webserver, scheduler, workers).

3. Import the `Code/Deployment/airflow_dags.py` file into your Airflow `dags` directory.

## Conclusion
Thank you for choosing the Decision Analytics Platform for Airbnb. Whether you're a data enthusiast, host, or traveler, our platform empowers you with the insights and predictions you need to make informed decisions. Choose the installation method that suits you best and start exploring the world of Airbnb data today!

For any inquiries or support, feel free to contact me at [git@dmes.ml](mailto:git@dmes.ml).
