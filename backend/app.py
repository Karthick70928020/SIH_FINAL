import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
from packet_capture import PacketCapture
from ml_models import AnomalyDetector
from encryption import EncryptionManager
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smart-network-monitor-secret-key'
CORS(app, origins=["http://localhost:5173"])
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173"], logger=True, engineio_logger=True)

# Global instances
packet_capture = None
anomaly_detector = None
encryption_manager = None
config = Config()
capture_thread = None
is_capturing = False

def initialize_components():
    """Initialize all system components"""
    global anomaly_detector, encryption_manager
    
    try:
        anomaly_detector = AnomalyDetector(
            model_type=config.ml_model,
            feature_level=config.feature_level
        )
        encryption_manager = EncryptionManager(config.encryption_algorithm)
        logger.info("Components initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")

def packet_callback(packet_data):
    """Callback function for when a packet is captured"""
    try:
        # Process packet through ML models
        if anomaly_detector:
            packet_data['is_anomaly'], packet_data['anomaly_score'] = anomaly_detector.predict(packet_data)
        else:
            packet_data['is_anomaly'] = False
            packet_data['anomaly_score'] = 0.0
        
        # Emit packet to frontend
        socketio.emit('packet_captured', packet_data)
        logger.debug(f"Packet emitted: {packet_data['id']}")
        
    except Exception as e:
        logger.error(f"Error processing packet: {e}")

def capture_worker():
    """Worker thread for packet capture"""
    global packet_capture, is_capturing
    
    try:
        packet_capture = PacketCapture(
            interface=config.network_interface,
            callback=packet_callback
        )
        
        logger.info(f"Starting packet capture on interface: {config.network_interface}")
        packet_capture.start_capture()
        
    except Exception as e:
        logger.error(f"Capture worker error: {e}")
        is_capturing = False
        socketio.emit('capture_error', {'error': str(e)})

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify({
        'status': 'running',
        'capturing': is_capturing,
        'config': config.to_dict(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Get or update configuration"""
    if request.method == 'GET':
        return jsonify(config.to_dict())
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            config.update(data)
            
            # Reinitialize components if needed
            if any(key in data for key in ['ml_model', 'feature_level', 'encryption_algorithm']):
                initialize_components()
            
            return jsonify({'status': 'success', 'config': config.to_dict()})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/interfaces', methods=['GET'])
def get_interfaces():
    """Get available network interfaces"""
    try:
        interfaces = PacketCapture.get_available_interfaces()
        return jsonify(interfaces)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_logs():
    """Export captured logs with encryption"""
    try:
        data = request.get_json()
        logs = data.get('logs', [])
        format_type = data.get('format', 'json')  # json or csv
        
        if not logs:
            return jsonify({'error': 'No logs to export'}), 400
        
        # Prepare data
        if format_type == 'json':
            export_data = json.dumps(logs, indent=2)
            filename = f"network_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        else:
            # Convert to CSV format
            import pandas as pd
            df = pd.DataFrame(logs)
            export_data = df.to_csv(index=False)
            filename = f"network_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Encrypt data
        if encryption_manager:
            encrypted_data = encryption_manager.encrypt(export_data.encode())
            filename = filename.replace('.', '_encrypted.')
        else:
            encrypted_data = export_data.encode()
        
        # Return encrypted data as base64
        import base64
        encoded_data = base64.b64encode(encrypted_data).decode()
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'data': encoded_data,
            'encrypted': encryption_manager is not None
        })
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connected', {'status': 'connected', 'timestamp': datetime.now().isoformat()})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('start_capture')
def handle_start_capture(data=None):
    """Start packet capture"""
    global capture_thread, is_capturing
    
    try:
        if is_capturing:
            emit('capture_status', {'status': 'already_running'})
            return
        
        is_capturing = True
        capture_thread = threading.Thread(target=capture_worker, daemon=True)
        capture_thread.start()
        
        emit('capture_status', {'status': 'started', 'timestamp': datetime.now().isoformat()})
        logger.info("Packet capture started")
        
    except Exception as e:
        is_capturing = False
        emit('capture_error', {'error': str(e)})
        logger.error(f"Failed to start capture: {e}")

@socketio.on('stop_capture')
def handle_stop_capture():
    """Stop packet capture"""
    global packet_capture, is_capturing
    
    try:
        is_capturing = False
        
        if packet_capture:
            packet_capture.stop_capture()
            packet_capture = None
        
        emit('capture_status', {'status': 'stopped', 'timestamp': datetime.now().isoformat()})
        logger.info("Packet capture stopped")
        
    except Exception as e:
        emit('capture_error', {'error': str(e)})
        logger.error(f"Failed to stop capture: {e}")

@socketio.on('update_config')
def handle_update_config(data):
    """Update configuration via WebSocket"""
    try:
        config.update(data)
        
        # Reinitialize components if needed
        if any(key in data for key in ['ml_model', 'feature_level', 'encryption_algorithm']):
            initialize_components()
        
        emit('config_updated', {'status': 'success', 'config': config.to_dict()})
        logger.info("Configuration updated via WebSocket")
        
    except Exception as e:
        emit('config_error', {'error': str(e)})
        logger.error(f"Config update error: {e}")

if __name__ == '__main__':
    logger.info("Starting Smart Network Monitor Backend")
    
    # Initialize components
    initialize_components()
    
    # Start the server
    socketio.run(
        app,
        host='127.0.0.1',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )