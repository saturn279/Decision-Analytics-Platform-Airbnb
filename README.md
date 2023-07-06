# Decision-Analytics-Platform-Airbnb
Generalized batch processing and analytics framework.
# Demo
[Client Interface](https://user-images.githubusercontent.com/101204171/206233456-49c86b3e-62a8-4cfa-9496-409603191465.webm)
# Installation
### Pre-deployed
   [Streamlit Cloud](https://saturn279-deploy-airbnb-streamlit-app-4za9hw.streamlitapp.com)
### Portable
#### Prerequisites

    pip install scikit-learn bs4 xgboost pandas requests numpy matplotlib streamlit 
#### Initilization
    git clone https://github.com/saturn279/Decision-Analytics-Platform-Airbnb
    cd Decision-Analytics-Platform-Airbnb/Code/Deployment
    streamlit run streamlit_internal.py 
#### In new terminal
    streamlit run streamlit_app.py

### Hadoop cluster
    install python3 >= 3.7
    install hadoop >= 3
    start hdfs e.g. bash run-hdfs.sh -s start

### Airflow
    install python3 >= 3.7
    install airflow >= 1.10
    start airflow webserver, scheduler, worker/s.
    import Code/Deployement/airflow_dags.py in AIRFLOW_HOME/dags

    
