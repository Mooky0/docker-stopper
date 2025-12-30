import docker
import threading
import time
from flask import Flask, render_template
import os
import dotenv

dotenv.load_dotenv()
app = Flask(__name__)
client = docker.from_env()



CONTAINER_NAME = os.getenv('CONTAINER_NAME', "test2")
PAUSE_DURATION = int(os.getenv('PAUSE_DURATION', 30))  # 10 seconds for testing; set to 1800 for 30 minutes

running = True

def update_running_status():
    global running
    container = client.containers.get(CONTAINER_NAME)
    running = container.status == 'running'

def restart_container(name):
    """Wait for the duration and then start the container."""
    print(f"Container {name} will restart in {PAUSE_DURATION / 60} minutes.")
    time.sleep(PAUSE_DURATION)
    print(f"Restarting container {name}...")
    container = client.containers.get(name)
    container.start()
    update_running_status()
    print(f"Container {name} restarted.")

@app.route('/')
def index():
    global running
    update_running_status()

    return render_template('index.html', running=running)

@app.route('/disable', methods=['POST'])
def disable():
    global running
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.stop()
        
        # Start the timer thread to turn it back on
        thread = threading.Thread(target=restart_container, args=(CONTAINER_NAME,))
        thread.start()
        
        update_running_status()
        return render_template('body.html', running=running, msg="Torrent szüneteltetve {} percre.".format(PAUSE_DURATION // 60))
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/start', methods=['POST'])
def start():
    global running
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.start()
        update_running_status()
        return render_template('body.html', running=running, msg="Torrent elindítva.")
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)