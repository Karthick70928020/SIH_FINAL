import os
import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging

logger = logging.getLogger(__name__)

class EncryptionManager:
    def __init__(self, algorithm='AES-256'):
        self.algorithm = algorithm
        self.private_key = None
        self.public_key = None
        self.aes_key = None
        
        self._initialize_keys()
    
    def _initialize_keys(self):
        """Initialize encryption keys based on selected algorithm"""
        try:
            if self.algorithm == 'RSA':
                self._generate_rsa_keys()
            elif self.algorithm in ['AES-256', 'AES-192']:
                self._generate_aes_key()
            elif self.algorithm == 'SHA':
                pass  # SHA is for hashing, not encryption
            
            logger.info(f"Encryption keys initialized for {self.algorithm}")
            
        except Exception as e:
            logger.error(f"Error initializing keys: {e}")
    
    def _generate_rsa_keys(self):
        """Generate RSA key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def _generate_aes_key(self):
        """Generate AES key"""
        if self.algorithm == 'AES-256':
            self.aes_key = os.urandom(32)  # 256 bits
        elif self.algorithm == 'AES-192':
            self.aes_key = os.urandom(24)  # 192 bits
    
    def encrypt(self, data):
        """Encrypt data using the selected algorithm"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            if self.algorithm == 'RSA':
                return self._encrypt_rsa(data)
            elif self.algorithm in ['AES-256', 'AES-192']:
                return self._encrypt_aes(data)
            elif self.algorithm == 'SHA':
                return self._hash_sha256(data)
            else:
                raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data  # Return original data if encryption fails
    
    def decrypt(self, encrypted_data):
        """Decrypt data using the selected algorithm"""
        try:
            if self.algorithm == 'RSA':
                return self._decrypt_rsa(encrypted_data)
            elif self.algorithm in ['AES-256', 'AES-192']:
                return self._decrypt_aes(encrypted_data)
            elif self.algorithm == 'SHA':
                raise ValueError("SHA is a one-way hash function, cannot decrypt")
            else:
                raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return encrypted_data  # Return original data if decryption fails
    
    def _encrypt_rsa(self, data):
        """Encrypt data using RSA"""
        if not self.public_key:
            raise ValueError("RSA public key not available")
        
        # RSA can only encrypt small amounts of data
        # For larger data, we'll use hybrid encryption (RSA + AES)
        if len(data) > 190:  # RSA-2048 can encrypt ~245 bytes, leave some margin
            # Generate temporary AES key
            temp_aes_key = os.urandom(32)
            
            # Encrypt data with AES
            encrypted_data = self._encrypt_aes_with_key(data, temp_aes_key)
            
            # Encrypt AES key with RSA
            encrypted_key = self.public_key.encrypt(
                temp_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Combine encrypted key and data
            return encrypted_key + b'|SEPARATOR|' + encrypted_data
        else:
            # Direct RSA encryption for small data
            return self.public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
    
    def _decrypt_rsa(self, encrypted_data):
        """Decrypt data using RSA"""
        if not self.private_key:
            raise ValueError("RSA private key not available")
        
        if b'|SEPARATOR|' in encrypted_data:
            # Hybrid decryption
            parts = encrypted_data.split(b'|SEPARATOR|', 1)
            encrypted_key = parts[0]
            encrypted_data = parts[1]
            
            # Decrypt AES key
            aes_key = self.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decrypt data with AES
            return self._decrypt_aes_with_key(encrypted_data, aes_key)
        else:
            # Direct RSA decryption
            return self.private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
    
    def _encrypt_aes(self, data):
        """Encrypt data using AES"""
        return self._encrypt_aes_with_key(data, self.aes_key)
    
    def _encrypt_aes_with_key(self, data, key):
        """Encrypt data using AES with specific key"""
        if not key:
            raise ValueError("AES key not available")
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad data to multiple of 16 bytes
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length]) * padding_length
        
        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + encrypted data
        return iv + encrypted_data
    
    def _decrypt_aes(self, encrypted_data):
        """Decrypt data using AES"""
        return self._decrypt_aes_with_key(encrypted_data, self.aes_key)
    
    def _decrypt_aes_with_key(self, encrypted_data, key):
        """Decrypt data using AES with specific key"""
        if not key:
            raise ValueError("AES key not available")
        
        # Extract IV and encrypted data
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def _hash_sha256(self, data):
        """Hash data using SHA-256"""
        return hashlib.sha256(data).digest()
    
    def get_public_key_pem(self):
        """Get public key in PEM format"""
        if not self.public_key:
            return None
        
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    
    def verify_data_integrity(self, data, hash_value):
        """Verify data integrity using hash"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        calculated_hash = self._hash_sha256(data)
        return calculated_hash == hash_value