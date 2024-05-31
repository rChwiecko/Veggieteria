from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
from EatingAction import setAddr, main, check_balance, init_asset_hub

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing purposes
socketio = SocketIO(app, cors_allowed_origins="*")

lock = threading.Lock()

def run_script(script_name, param):
    try:
        if script_name == 'EatingAction':
            main(socketio)  # Call the main function with the parameter
            return {'output': 'EatingAction script executed successfully'}
        elif script_name == 'SetAddr':
            setAddr(param)
            substrate = init_asset_hub()
            acc_balance = check_balance(substrate, 88228866, param)  # Make sure check_balance returns a serializable value
            return {'acc_balance': acc_balance, 'output': 'Change addr ran'}
        else:
            return {'error': 'Invalid script name'}
    except Exception as e:
        return {'error': str(e)}

@app.route('/run_script', methods=['POST'])
def run_script_endpoint():
    data = request.json
    script_name = data.get('script_name')
    param = data.get("wallet_addr")
    
    if script_name in ['EatingAction', 'SetAddr']:  # Add more script names as needed
        if lock.acquire(blocking=False):  # Try to acquire the lock without blocking
            try:
                result = run_script(script_name, param)
                return jsonify(result)
            finally:
                lock.release()  # Release the lock after the script finishes
        else:
            return jsonify({'error': 'Another script is currently running'}), 409
    else:
        return jsonify({'error': 'Invalid script name'}), 400

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
