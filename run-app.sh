#!/bin/bash

# Ensure the script exits on error
set -e

# Step 1: Start the ollama service in the background
echo "Starting Ollama service..."
ollama run llama2 &
OLLAMA_PID=$!

# Allow time for the service to initialize
sleep 5
echo "Ollama service started with PID $OLLAMA_PID."

# Step 2: Start the Streamlit app
echo "Starting Streamlit app..."
streamlit run ocr.py

# Wait for both processes
wait $OLLAMA_PID
