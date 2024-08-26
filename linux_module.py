import subprocess

def get_active_window_x():
    try:
        result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None

def get_chrome_url_x():
    try:
        # Use xdotool to simulate keypresses to copy the URL from the Chrome address bar
        subprocess.run(['xdotool', 'key', 'ctrl+l'])  # Select the address bar
        subprocess.run(['xdotool', 'key', 'ctrl+c'])  # Copy the URL to clipboard
        result = subprocess.run(['xclip', '-o'], capture_output=True, text=True)  # Read from clipboard
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting Chrome URL: {e}")
        return None
