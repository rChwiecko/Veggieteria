from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import threading
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

lock = threading.Lock()

# Define the path where your scripts are located
SCRIPT_PATH = '/Users/alexdang/Desktop/Veggieteria/Backend'  # Update this path accordingly

def run_script(script_name):
    try:
        script_full_path = os.path.join(SCRIPT_PATH, f'{script_name}.py')
        if not os.path.isfile(script_full_path):
            return {'error': f'Script {script_name}.py not found at {SCRIPT_PATH}'}
        
        result = subprocess.run(['python', script_full_path], capture_output=True, text=True)
        return {'output': result.stdout, 'error': result.stderr}
    except Exception as e:
        return {'error': str(e)}

@app.route('/run_script', methods=['POST'])
def run_script_endpoint():
    data = request.json
    script_name = data.get('script_name')
    
    if script_name in ['EatingAction', 'OtherScript']:  # Add more script names as needed
        if lock.acquire(blocking=False):  # Try to acquire the lock without blocking
            try:
                result = run_script(script_name)
                return jsonify(result)
            finally:
                lock.release()  # Release the lock after the script finishes
        else:
            return jsonify({'error': 'Another script is currently running'}), 409
    else:
        return jsonify({'error': 'Invalid script name'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
