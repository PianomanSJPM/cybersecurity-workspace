import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import gzip
import tarfile
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupEncryption:
    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the backup encryption module."""
        self.config_path = config_path
        self.config = self._load_config()
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {self.config_path}")
            return {}
    
    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate a new one."""
        key_path = Path('config/backup.key')
        
        if key_path.exists():
            try:
                with open(key_path, 'rb') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error loading key: {e}")
                return self._generate_key()
        else:
            return self._generate_key()
    
    def _generate_key(self) -> bytes:
        """Generate a new encryption key."""
        try:
            key = Fernet.generate_key()
            key_path = Path('config/backup.key')
            key_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(key_path, 'wb') as f:
                f.write(key)
            
            logger.info("Generated new encryption key")
            return key
        except Exception as e:
            logger.error(f"Error generating key: {e}")
            raise
    
    def encrypt_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Encrypt a file and optionally compress it."""
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Determine output path if not provided
            if output_path is None:
                output_path = str(input_path) + '.enc'
            
            # Read input file
            with open(input_path, 'rb') as f:
                data = f.read()
            
            # Compress if enabled
            if self.config.get('compress_backups', True):
                data = gzip.compress(data)
            
            # Encrypt data
            encrypted_data = self.fernet.encrypt(data)
            
            # Write encrypted data
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)
            
            logger.info(f"Encrypted file: {input_path} -> {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error encrypting file: {e}")
            raise
    
    def decrypt_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Decrypt a file and optionally decompress it."""
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Determine output path if not provided
            if output_path is None:
                output_path = str(input_path).replace('.enc', '')
            
            # Read encrypted data
            with open(input_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            data = self.fernet.decrypt(encrypted_data)
            
            # Decompress if needed
            try:
                data = gzip.decompress(data)
            except:
                pass  # Not compressed
            
            # Write decrypted data
            with open(output_path, 'wb') as f:
                f.write(data)
            
            logger.info(f"Decrypted file: {input_path} -> {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error decrypting file: {e}")
            raise
    
    def encrypt_directory(self, input_dir: str, output_path: Optional[str] = None) -> str:
        """Encrypt and compress a directory."""
        try:
            input_dir = Path(input_dir)
            if not input_dir.exists():
                raise FileNotFoundError(f"Input directory not found: {input_dir}")
            
            # Create temporary tar file
            temp_tar = str(input_dir) + '.tar'
            temp_tar_path = Path(temp_tar)
            if temp_tar_path.exists():
                if temp_tar_path.is_dir():
                    shutil.rmtree(temp_tar_path)
                else:
                    temp_tar_path.unlink()
            with tarfile.open(temp_tar, 'w') as tar:
                tar.add(input_dir, arcname=input_dir.name)
            
            # Encrypt the tar file
            encrypted_path = self.encrypt_file(temp_tar, output_path)
            
            # Clean up temporary file
            os.remove(temp_tar)
            
            return encrypted_path
        except Exception as e:
            logger.error(f"Error encrypting directory: {e}")
            raise
    
    def decrypt_directory(self, input_path: str, output_dir: Optional[str] = None) -> str:
        """Decrypt and decompress a directory."""
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Determine output directory if not provided
            if output_dir is None:
                output_dir = str(input_path).replace('.enc', '')
            
            # Create temporary directory for decrypted tar
            temp_dir = Path('temp_decrypt')
            temp_dir.mkdir(exist_ok=True)
            temp_tar = temp_dir / 'decrypted.tar'
            
            # Decrypt the file
            self.decrypt_file(input_path, str(temp_tar))
            
            # Extract the tar file
            with tarfile.open(temp_tar, 'r') as tar:
                tar.extractall(path=output_dir)
            
            # Clean up temporary files
            shutil.rmtree(temp_dir)
            
            return output_dir
        except Exception as e:
            logger.error(f"Error decrypting directory: {e}")
            raise
    
    def rotate_keys(self) -> None:
        """Rotate encryption keys and re-encrypt all backups."""
        try:
            # Generate new key
            new_key = Fernet.generate_key()
            new_fernet = Fernet(new_key)
            
            # Get all encrypted backups
            backup_dir = Path(self.config.get('backup_location', 'backups'))
            encrypted_files = list(backup_dir.glob('**/*.enc'))
            
            # Re-encrypt each backup with new key
            for file in encrypted_files:
                try:
                    # Decrypt with old key
                    with open(file, 'rb') as f:
                        encrypted_data = f.read()
                    data = self.fernet.decrypt(encrypted_data)
                    
                    # Encrypt with new key
                    new_encrypted_data = new_fernet.encrypt(data)
                    
                    # Write re-encrypted data
                    with open(file, 'wb') as f:
                        f.write(new_encrypted_data)
                    
                    logger.info(f"Re-encrypted backup: {file}")
                except Exception as e:
                    logger.error(f"Error re-encrypting backup {file}: {e}")
            
            # Save new key
            key_path = Path('config/backup.key')
            with open(key_path, 'wb') as f:
                f.write(new_key)
            
            # Update instance variables
            self.key = new_key
            self.fernet = new_fernet
            
            logger.info("Successfully rotated encryption keys")
        except Exception as e:
            logger.error(f"Error rotating keys: {e}")
            raise

if __name__ == '__main__':
    # Example usage
    encryption = BackupEncryption()
    
    # Encrypt a file
    encrypted_file = encryption.encrypt_file('example.txt')
    
    # Decrypt the file
    decrypted_file = encryption.decrypt_file(encrypted_file)
    
    # Encrypt a directory
    encrypted_dir = encryption.encrypt_directory('example_dir')
    
    # Decrypt the directory
    decrypted_dir = encryption.decrypt_directory(encrypted_dir)
    
    # Rotate keys
    encryption.rotate_keys() 