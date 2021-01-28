mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
enableWebsocketCompression=false
[browser]
serverAddress='https://datanecdotes-psb.herokuapp.com/'
serverPort= $PORT
" > ~/.streamlit/config.toml
