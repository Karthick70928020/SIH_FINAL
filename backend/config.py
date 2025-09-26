import json
import os
import logging

logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.data = {
            'network_interface': 'eth0',
            'buffer_size': 1000,
            'analysis_depth': 'intermediate',
            'ml_model': 'both',
            'feature_level': 'standard',
            'encryption_algorithm': 'AES-256'
        }
        
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    file_data = json.load(f)
                    self.data.update(file_data)
                    logger.info(f"Configuration loaded from {self.config_file}")
            else:
                logger.info("Using default configuration")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def update(self, new_data):
        """Update configuration with new data"""
        self.data.update(new_data)
        self.save_config()
    
    def to_dict(self):
        """Return configuration as dictionary"""
        return self.data.copy()
    
    @property
    def network_interface(self):
        return self.data['network_interface']
    
    @property
    def buffer_size(self):
        return self.data['buffer_size']
    
    @property
    def analysis_depth(self):
        return self.data['analysis_depth']
    
    @property
    def ml_model(self):
        return self.data['ml_model']
    
    @property
    def feature_level(self):
        return self.data['feature_level']
    
    @property
    def encryption_algorithm(self):
        return self.data['encryption_algorithm']