# Use a Python base image
FROM python:3.7

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir scikit-learn bs4 xgboost pandas requests seaborn numpy matplotlib streamlit

# Expose the default Streamlit port
EXPOSE 8501
EXPOSE 8502

# Start both Streamlit apps in the background
CMD streamlit run /app/Code/Deployment/streamlit_internal.py & streamlit run /app/Code/Deployment/streamlit_app.py && tail -f /dev/null
