import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ransomware.ransomware_sim import RansomwareSimulation
from src.keylogger.keylogger_sim import KeyloggerSimulation

def test_ransomware():
    """Test the ransomware simulation with sample files."""
    # Setup test environment
    test_dir = "./test_files"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Create test files if they don't exist
    if not os.listdir(test_dir):
        with open(os.path.join(test_dir, "document1.txt"), "w") as f:
            f.write("Test content 1")
        with open(os.path.join(test_dir, "document2.txt"), "w") as f:
            f.write("Test content 2")
    
    # Create ransomware instance
    ransomware = RansomwareSimulation(test_dir)
    
    # Simulate attack
    print("Starting ransomware simulation...")
    ransomware.simulate_attack()
    
    # Check if files are encrypted
    encrypted_files = [f for f in os.listdir(test_dir) if f.endswith('.encrypted')]
    print(f"Encrypted files: {encrypted_files}")
    
    # Simulate recovery
    print("\nSimulating recovery...")
    ransomware.simulate_recovery(ransomware.key)
    
    # Check if files are recovered
    recovered_files = [f for f in os.listdir(test_dir) if not f.endswith('.encrypted')]
    print(f"Recovered files: {recovered_files}")

def test_keylogger():
    """Test the keylogger simulation briefly."""
    print("Starting keylogger simulation...")
    print("Will run for 10 seconds. Type something...")
    
    # Create keylogger instance
    keylogger = KeyloggerSimulation("test_keylog.txt")
    
    # Run for 10 seconds
    import threading
    import time
    
    stop_thread = threading.Event()
    
    def stop_after_timeout():
        time.sleep(10)
        keylogger.stop()
        stop_thread.set()
    
    # Start timeout thread
    timeout_thread = threading.Thread(target=stop_after_timeout)
    timeout_thread.start()
    
    # Start keylogger
    try:
        keylogger.start()
    except Exception as e:
        print(f"Error: {e}")
    
    # Wait for timeout
    stop_thread.wait()
    
    # Check the log file
    if os.path.exists("test_keylog.txt"):
        with open("test_keylog.txt", "r") as f:
            print("\nCaptured keystrokes:")
            print(f.read())
        os.remove("test_keylog.txt")

if __name__ == "__main__":
    print("Running Malware Simulation Tests")
    print("=" * 30)
    
    # Run ransomware test
    print("\nRansomware Test:")
    test_ransomware()
    
    # Run keylogger test
    print("\nKeylogger Test:")
    test_keylogger()
    
    print("\nTests completed!")