"""
Password Manager Module
A secure password management system using Fernet encryption.

This module provides a secure way to store and manage passwords using
cryptographic encryption. It uses PBKDF2 for key derivation and Fernet
for symmetric encryption of password data.
"""

import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass

class PasswordManager:
    """A secure password management system.
    
    This class provides methods for securely storing, retrieving, and managing
    passwords using cryptographic encryption. All passwords are encrypted at rest
    and require a master password for access.
    """
    
    def __init__(self, storage_file='passwords.enc'):
        """Initialize the password manager.
        
        Args:
            storage_file (str): Path to the encrypted password storage file
        """
        self.storage_file = storage_file
        self.key = None
        self.fernet = None
        self.passwords = {}

    def _generate_key(self, master_password):
        """Generate encryption key from master password using PBKDF2.
        
        Args:
            master_password (str): The master password for encryption
            
        Returns:
            bytes: The derived encryption key
            
        Note:
            In a production environment, the salt should be randomly generated
            and stored securely. This implementation uses a fixed salt for
            demonstration purposes only.
        """
        salt = b'fixed_salt'  # WARNING: Use random salt in production
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    def initialize(self, master_password):
        """Initialize the password manager with a master password.
        
        Args:
            master_password (str): The master password for encryption
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.key = self._generate_key(master_password)
            self.fernet = Fernet(self.key)
            if os.path.exists(self.storage_file):
                self.load_passwords()
            return True
        except Exception as e:
            print(f"Error initializing password manager: {str(e)}")
            return False

    def load_passwords(self):
        """Load encrypted passwords from the storage file.
        
        Returns:
            bool: True if loading successful, False otherwise
        """
        try:
            with open(self.storage_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.passwords = json.loads(decrypted_data.decode())
            return True
        except Exception as e:
            print(f"Error loading passwords: {str(e)}")
            return False

    def save_passwords(self):
        """Save encrypted passwords to the storage file.
        
        Returns:
            bool: True if saving successful, False otherwise
        """
        try:
            encrypted_data = self.fernet.encrypt(json.dumps(self.passwords).encode())
            with open(self.storage_file, 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Error saving passwords: {str(e)}")
            return False

    def add_password(self, website, username, password):
        """Add a new password entry for a website.
        
        Args:
            website (str): The website or service name
            username (str): The username or email
            password (str): The password to store
            
        Returns:
            bool: True if addition successful, False otherwise
        """
        try:
            self.passwords[website] = {
                'username': username,
                'password': password
            }
            self.save_passwords()
            return True
        except Exception as e:
            print(f"Error adding password: {str(e)}")
            return False

    def get_password(self, website):
        """Retrieve stored credentials for a website.
        
        Args:
            website (str): The website or service name
            
        Returns:
            dict: Dictionary containing username and password, or None if not found
        """
        try:
            return self.passwords.get(website)
        except Exception as e:
            print(f"Error retrieving password: {str(e)}")
            return None

    def delete_password(self, website):
        """Delete stored credentials for a website.
        
        Args:
            website (str): The website or service name
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            if website in self.passwords:
                del self.passwords[website]
                self.save_passwords()
                return True
            return False
        except Exception as e:
            print(f"Error deleting password: {str(e)}")
            return False

    def list_websites(self):
        """List all websites with stored credentials.
        
        Returns:
            list: List of website names
        """
        try:
            return list(self.passwords.keys())
        except Exception as e:
            print(f"Error listing websites: {str(e)}")
            return []

    def update_password(self, website, username, password):
        """Update existing credentials for a website.
        
        Args:
            website (str): The website or service name
            username (str): The new username or email
            password (str): The new password
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            if website in self.passwords:
                self.passwords[website] = {
                    'username': username,
                    'password': password
                }
                self.save_passwords()
                return True
            return False
        except Exception as e:
            print(f"Error updating password: {str(e)}")
            return False 