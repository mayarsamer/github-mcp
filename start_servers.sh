#!/bin/bash

echo "Starting main.py server..."
python src/main.py &
MAIN_PID=$!

echo "Starting LLM_client with uvicorn..."
uvicorn src.LLM_client:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

echo "Starting Streamlit app..."
streamlit run src/streamlit_app1.py &
STREAMLIT_PID=$!

echo "All servers started:"
echo "main.py PID: $MAIN_PID"
echo "uvicorn PID: $UVICORN_PID"
echo "streamlit PID: $STREAMLIT_PID"

wait $MAIN_PID $UVICORN_PID $STREAMLIT_PID
