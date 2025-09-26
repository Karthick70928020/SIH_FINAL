# Smart Network Monitor

A comprehensive full-stack application for real-time network monitoring with machine learning-powered anomaly detection and secure log export capabilities.

![Network Monitor Dashboard](https://images.pexels.com/photos/11035471/pexels-photo-11035471.jpeg?auto=compress&cs=tinysrgb&w=1200)

## Features

### 🔍 Real-time Network Monitoring
- Live packet capture using PyShark
- Real-time data streaming via WebSockets
- Support for multiple network interfaces
- Configurable packet buffer sizes

### 🤖 Machine Learning Anomaly Detection
- **Autoencoder**: Deep learning model for unsupervised anomaly detection
- **Isolation Forest**: Ensemble method for outlier detection
- Configurable feature extraction levels
- Real-time anomaly scoring and alerts

### ⚙️ Advanced Configuration
- **System Settings**: Buffer size, analysis depth, dark mode
- **Network Configuration**: Interface selection, packet filtering
- **ML Model Settings**: Model selection and feature levels
- **Security Options**: Multiple encryption algorithms

### 🔒 Enterprise Security
- **Encryption Support**: RSA, AES-256, AES-192, SHA-256
- **Secure Export**: Encrypted log export in JSON/CSV formats
- **Data Integrity**: Hash verification for exported data
- **Secure Transport**: TLS-encrypted WebSocket connections

### 🎨 Modern Frontend
- Built with React, TypeScript, and Tailwind CSS
- Smooth animations with Framer Motion
- Real-time charts and visualizations
- Dark mode support
- Fully responsive design

## Tech Stack

### Frontend
- **Framework**: React 18 + Vite + TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Routing**: React Router
- **Icons**: Lucide React

### Backend
- **Framework**: Flask + Flask-SocketIO
- **Packet Capture**: PyShark
- **Machine Learning**: scikit-learn + TensorFlow
- **Security**: Cryptography library
- **Data Processing**: Pandas + NumPy

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ and pip
- Network capture tools (optional: tshark/wireshark)

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python start.py
```

The backend will be available at `http://127.0.0.1:5000`

## Configuration Options

### Network Settings
- **Interface Selection**: Choose from available network interfaces
- **Buffer Size**: Control memory usage (100-10,000 packets)
- **Analysis Depth**: Basic, Intermediate, or Deep analysis

### Machine Learning
- **Model Types**: 
  - Autoencoder: Neural network for pattern learning
  - Isolation Forest: Tree-based anomaly detection
  - Both: Combined approach for higher accuracy
- **Feature Levels**: Advanced, Standard, or Low complexity

### Security
- **Encryption Algorithms**:
  - RSA: Asymmetric encryption with 2048-bit keys
  - AES-256: Advanced Encryption Standard 256-bit
  - AES-192: Advanced Encryption Standard 192-bit
  - SHA-256: Secure hash for data integrity

## API Documentation

### REST Endpoints
- `GET /api/status` - System status and health check
- `GET /api/config` - Current configuration
- `POST /api/config` - Update configuration
- `GET /api/interfaces` - Available network interfaces
- `POST /api/export` - Export encrypted logs

### WebSocket Events
- `connect` - Client connection established
- `start_capture` - Begin packet capture
- `stop_capture` - End packet capture
- `packet_captured` - New packet data (real-time)
- `update_config` - Configuration changes

## Project Structure

```
smart-network-monitor/
├── src/                     # Frontend source
│   ├── components/          # React components
│   ├── pages/              # Application pages
│   ├── contexts/           # React context providers
│   └── types/              # TypeScript definitions
├── backend/                # Python backend
│   ├── app.py             # Main Flask application
│   ├── packet_capture.py  # Network capture logic
│   ├── ml_models.py       # Machine learning models
│   ├── encryption.py      # Security and encryption
│   └── config.py          # Configuration management
└── README.md              # Project documentation
```

## Security Features

### Data Protection
- All network logs are encrypted before export
- Multiple encryption algorithms supported
- Hash-based integrity verification
- Secure key generation and management

### Network Security
- WebSocket connections use secure transport
- No sensitive data stored in local storage
- Configurable security levels
- Real-time threat detection

### Privacy
- Local processing - no data sent to external servers
- Configurable data retention policies
- User-controlled encryption settings
- Anonymous packet analysis

## Performance Features

- **Efficient Memory Usage**: Configurable buffer sizes
- **Real-time Processing**: Sub-second packet analysis
- **Scalable Architecture**: Handles high packet volumes
- **Optimized Rendering**: Smooth 60fps animations
- **Progressive Loading**: Incremental data updates

## Troubleshooting

### Common Issues

**Permission Errors (Linux/macOS)**:
```bash
# Add user to wireshark group
sudo usermod -a -G wireshark $USER
# Logout and login again
```

**Port Already in Use**:
```bash
# Kill processes using ports 5000 or 5173
sudo lsof -ti:5000 | xargs kill -9
sudo lsof -ti:5173 | xargs kill -9
```

**Missing Dependencies**:
```bash
# Frontend
npm install

# Backend
pip install -r backend/requirements.txt
```

### Demo Mode
If packet capture is not available, the system automatically switches to demo mode with simulated network data for testing purposes.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyShark team for excellent packet capture capabilities
- Recharts for beautiful data visualizations
- Tailwind CSS for utility-first styling
- The open-source community for inspiration and tools