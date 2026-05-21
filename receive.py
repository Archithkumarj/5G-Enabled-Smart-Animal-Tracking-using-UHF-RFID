import socket
import datetime
import threading
from flask import Flask, render_template_string

# UDP Server configuration
UDP_IP = ""  # Listen on the same IP
UDP_PORT = 5005           # Same port as client

# Web server configuration
WEB_PORT = 8080

# Shared data store for received messages
messages = []

# Flask app setup
app = Flask(__name__)

# HTML template for displaying messages
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Animal Identification Data</title>
    <meta http-equiv="refresh" content="5"> 
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .message { margin: 10px 0; padding: 10px; border: 1px solid #ccc; }
        .timestamp { color: #555; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>Animal Identification Data</h1>
    {% for msg in messages %}
        <div class="message">
            <div class="timestamp">{{ msg.timestamp }}</div>
            <pre>{{ msg.content }}</pre>
        </div>
    {% endfor %}
</body>
</html>
"""

def start_udp_server():
    """Start UDP server to receive EPC data"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((UDP_IP, UDP_PORT))
            print(f"UDP Server listening on {UDP_IP}:{UDP_PORT}")
            print("Waiting for data...")
            print("-" * 50)
            
            while True:
                try:
                    data, addr = sock.recvfrom(4096)
                    message = data.decode('utf-8')
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Store message with timestamp
                    messages.append({"timestamp": timestamp, "content": message})
                    # Keep only the last 50 messages to avoid memory issues
                    if len(messages) > 50:
                        messages.pop(0)
                    
                    # Print to console
                    print(f"[{timestamp}] Data received from {addr[0]}:{addr[1]}")
                    print("Message content:")
                    print(message)
                    print("-" * 50)
                    
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    
    except Exception as e:
        print(f"Error starting UDP server: {e}")

@app.route('/')
def display_data():
    """Render the webpage with received messages"""
    return render_template_string(HTML_TEMPLATE, messages=messages)

def run_flask():
    """Run Flask web server"""
    print(f"Starting web server on http://0.0.0.0:{WEB_PORT}")
    app.run(host='0.0.0.0', port=WEB_PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start UDP server in a separate thread
    udp_thread = threading.Thread(target=start_udp_server, daemon=True)
    udp_thread.start()
    
    # Start Flask web server in the main thread
    run_flask()
