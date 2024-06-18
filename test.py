import keyboard

# Define your function to be called when the hotkey is pressed
def my_function():
    print("Hotkey pressed!")

# Add a hotkey using keyboard.add_hotkey
# Syntax: keyboard.add_hotkey(hotkey, callback_function, args=(), suppress=False, timeout=1, trigger_on_release=False)
# Here, 'hotkey' can be a combination of keys or a single key
# Use the number key you want by specifying its key name or code as a string
keyboard.add_hotkey('1', my_function)  # Example with the number 1 key

# You can add more hotkeys as needed
keyboard.add_hotkey('2', my_function)  # Example with the number 2 key

# Start the keyboard listener
keyboard.wait('esc')  # This will wait until 'esc' key is pressed to stop the program