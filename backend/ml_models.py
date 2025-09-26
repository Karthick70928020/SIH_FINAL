import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import logging
import pickle
import os

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, model_type='both', feature_level='standard'):
        self.model_type = model_type
        self.feature_level = feature_level
        self.scaler = StandardScaler()
        self.isolation_forest = None
        self.autoencoder = None
        self.is_trained = False
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models"""
        try:
            if self.model_type in ['isolation_forest', 'both']:
                self.isolation_forest = IsolationForest(
                    contamination=0.1,  # Expect 10% anomalies
                    random_state=42
                )
            
            if self.model_type in ['autoencoder', 'both']:
                self._create_autoencoder()
            
            logger.info(f"Initialized models: {self.model_type}")
            
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
    
    def _create_autoencoder(self, input_dim=10):
        """Create autoencoder model"""
        try:
            # Define autoencoder architecture
            input_layer = Input(shape=(input_dim,))
            
            # Encoder
            encoded = Dense(8, activation='relu')(input_layer)
            encoded = Dense(4, activation='relu')(encoded)
            
            # Decoder
            decoded = Dense(8, activation='relu')(encoded)
            decoded = Dense(input_dim, activation='sigmoid')(decoded)
            
            # Create model
            self.autoencoder = Model(input_layer, decoded)
            self.autoencoder.compile(optimizer='adam', loss='mse')
            
            logger.info("Autoencoder model created")
            
        except Exception as e:
            logger.error(f"Error creating autoencoder: {e}")
    
    def extract_features(self, packet_data):
        """Extract features from packet data"""
        try:
            features = []
            
            # Basic features
            features.append(packet_data.get('length', 0))
            
            # Protocol encoding (simple hash-based)
            protocol = packet_data.get('protocol', 'unknown')
            features.append(hash(protocol) % 1000)
            
            # IP address features (convert to numeric)
            src_ip = packet_data.get('source_ip', '0.0.0.0')
            dst_ip = packet_data.get('destination_ip', '0.0.0.0')
            
            try:
                src_parts = [int(x) for x in src_ip.split('.')]
                dst_parts = [int(x) for x in dst_ip.split('.')]
                features.extend(src_parts[:4])
                features.extend(dst_parts[:4])
            except:
                # Fallback for non-IPv4 addresses
                features.extend([0, 0, 0, 0])  # src
                features.extend([0, 0, 0, 0])  # dst
            
            # Ensure we have exactly 10 features
            while len(features) < 10:
                features.append(0)
            features = features[:10]
            
            # Additional features based on level
            if self.feature_level == 'advanced':
                # Add time-based features
                import datetime
                now = datetime.datetime.now()
                features.extend([
                    now.hour,
                    now.minute,
                    now.weekday()
                ])
            elif self.feature_level == 'standard':
                features.extend([0, 0, 0])
            else:  # low
                features.extend([0, 0, 0])
            
            return np.array(features[:13]).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Feature extraction error: {e}")
            return np.zeros((1, 13))
    
    def train_models(self, training_data):
        """Train the anomaly detection models"""
        try:
            if not training_data:
                logger.warning("No training data provided")
                return
            
            # Extract features for all training data
            features = []
            for packet in training_data:
                feature_vector = self.extract_features(packet)
                features.append(feature_vector[0])
            
            features = np.array(features)
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train Isolation Forest
            if self.isolation_forest:
                self.isolation_forest.fit(features_scaled)
                logger.info("Isolation Forest trained")
            
            # Train Autoencoder
            if self.autoencoder and len(features_scaled) > 0:
                self.autoencoder.fit(
                    features_scaled,
                    features_scaled,
                    epochs=50,
                    batch_size=32,
                    verbose=0,
                    validation_split=0.2
                )
                logger.info("Autoencoder trained")
            
            self.is_trained = True
            
        except Exception as e:
            logger.error(f"Training error: {e}")
    
    def predict(self, packet_data):
        """Predict if packet is anomalous"""
        try:
            # Extract features
            features = self.extract_features(packet_data)
            
            # If models aren't trained, use simple rule-based detection
            if not self.is_trained:
                return self._rule_based_detection(packet_data)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            anomaly_scores = []
            predictions = []
            
            # Isolation Forest prediction
            if self.isolation_forest:
                if_pred = self.isolation_forest.predict(features_scaled)[0]
                if_score = self.isolation_forest.score_samples(features_scaled)[0]
                predictions.append(if_pred == -1)  # -1 means anomaly
                anomaly_scores.append(abs(if_score))
            
            # Autoencoder prediction
            if self.autoencoder:
                reconstruction = self.autoencoder.predict(features_scaled, verbose=0)
                mse = np.mean(np.power(features_scaled - reconstruction, 2))
                threshold = 0.1  # Adjustable threshold
                predictions.append(mse > threshold)
                anomaly_scores.append(mse)
            
            # Combine predictions
            if predictions:
                is_anomaly = any(predictions)
                avg_score = np.mean(anomaly_scores) if anomaly_scores else 0.0
            else:
                is_anomaly, avg_score = self._rule_based_detection(packet_data)
            
            return is_anomaly, float(avg_score)
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return False, 0.0
    
    def _rule_based_detection(self, packet_data):
        """Simple rule-based anomaly detection for fallback"""
        try:
            anomaly_score = 0.0
            is_anomaly = False
            
            # Check packet size
            length = packet_data.get('length', 0)
            if length > 8000 or length < 64:  # Unusually large or small packets
                anomaly_score += 0.5
                is_anomaly = True
            
            # Check for suspicious protocols
            protocol = packet_data.get('protocol', '').upper()
            suspicious_protocols = ['UNKNOWN', 'MALFORMED']
            if protocol in suspicious_protocols:
                anomaly_score += 0.3
                is_anomaly = True
            
            # Check for private IP to external communication patterns
            src_ip = packet_data.get('source_ip', '')
            dst_ip = packet_data.get('destination_ip', '')
            
            if src_ip.startswith('192.168.') and not dst_ip.startswith('192.168.'):
                if length > 5000:  # Large outbound packet
                    anomaly_score += 0.2
            
            return is_anomaly, min(anomaly_score, 1.0)
            
        except Exception as e:
            logger.error(f"Rule-based detection error: {e}")
            return False, 0.0
    
    def save_models(self, filepath):
        """Save trained models to disk"""
        try:
            model_data = {
                'scaler': self.scaler,
                'isolation_forest': self.isolation_forest,
                'model_type': self.model_type,
                'feature_level': self.feature_level,
                'is_trained': self.is_trained
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            # Save autoencoder separately if it exists
            if self.autoencoder:
                ae_path = filepath.replace('.pkl', '_autoencoder.h5')
                self.autoencoder.save(ae_path)
            
            logger.info(f"Models saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self, filepath):
        """Load trained models from disk"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.scaler = model_data['scaler']
            self.isolation_forest = model_data['isolation_forest']
            self.model_type = model_data['model_type']
            self.feature_level = model_data['feature_level']
            self.is_trained = model_data['is_trained']
            
            # Load autoencoder separately if it exists
            ae_path = filepath.replace('.pkl', '_autoencoder.h5')
            if os.path.exists(ae_path):
                self.autoencoder = tf.keras.models.load_model(ae_path)
            
            logger.info(f"Models loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")