mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
[browser]
serverAddress='thedatanecdotes'
" > ~/.streamlit/config.toml
