mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
enableWebsocketCompression=false
[browser]
serverAddress='thedatanecdotes'
" > ~/.streamlit/config.toml
