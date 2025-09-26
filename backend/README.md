# Smart Network Monitor Backend

## Overview

This Python backend provides real-time network packet capture, machine learning-based anomaly detection, and secure log export functionality for the Smart Network Monitor application.

## Features

- **Real-time Packet Capture**: Uses PyShark to capture live network packets
- **Machine Learning**: Implements Autoencoder and Isolation Forest for anomaly detection
- **WebSocket Communication**: Real-time data streaming to frontend
- **Encryption**: Multiple encryption algorithms (RSA, AES-256, AES-192, SHA-256)
- **Secure Export**: Encrypted log export in JSON/CSV formats

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install system dependencies for packet capture:
```bash
# On Ubuntu/Debian
sudo apt-get install tshark

# On macOS
brew install wireshark
```

## Running the Backend

```bash
python app.py
```

The backend will start on `http://127.0.0.1:5000` with WebSocket support.

## API Endpoints

- `GET /api/status` - Get system status
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `GET /api/interfaces` - Get available network interfaces
- `POST /api/export` - Export encrypted logs

## WebSocket Events

- `connect` - Client connection established
- `start_capture` - Start packet capture
- `stop_capture` - Stop packet capture
- `update_config` - Update configuration
- `packet_captured` - New packet captured (emitted to clients)

## Configuration

The backend supports the following configuration options:

- `network_interface`: Network interface to monitor (default: 'eth0')
- `buffer_size`: Number of packets to keep in memory (default: 1000)
- `analysis_depth`: Analysis level ('basic', 'intermediate', 'deep')
- `ml_model`: ML model to use ('autoencoder', 'isolation_forest', 'both')
- `feature_level`: Feature extraction level ('advanced', 'standard', 'low')
- `encryption_algorithm`: Encryption method ('RSA', 'AES-256', 'AES-192', 'SHA')

## Security Features

- All exported logs are automatically encrypted
- WebSocket connections support secure transport
- Data integrity verification using hash functions
- Multiple encryption algorithms available

## Machine Learning Models

### Autoencoder
- Deep learning model for unsupervised anomaly detection
- Learns normal network patterns and identifies deviations
- Uses reconstruction error as anomaly score

### Isolation Forest
- Ensemble method for outlier detection
- Isolates anomalies by randomly selecting features
- Effective for high-dimensional data

## File Structure

```
backend/
├── app.py              # Main Flask application
├── packet_capture.py   # Network packet capture
├── ml_models.py        # Machine learning models
├── encryption.py       # Encryption and security
├── config.py           # Configuration management
└── requirements.txt    # Python dependencies
```

## Troubleshooting

### Permission Issues
If you encounter permission errors during packet capture:
```bash
# Add your user to the wireshark group
sudo usermod -a -G wireshark $USER
# Logout and login again
```

### Interface Not Found
Check available interfaces:
```bash
# List network interfaces
ip link show
# or
ifconfig -a
```

### Demo Mode
If packet capture fails, the system automatically switches to demo mode, generating simulated packets for testing purposes.