from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")

# Enable logging for performance
caps = DesiredCapabilities().CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to Google Maps
driver.get("https://www.google.com/maps")  

def get_location():
    # Execute JavaScript to request geolocation
    driver.execute_script("navigator.geolocation.getCurrentPosition(function(position) {"
                          "console.log('Latitude: ' + position.coords.latitude + ', Longitude: ' + position.coords.longitude);"
                          "});")

    time.sleep(2)  # Short pause for the results to load

    # Retrieve performance logs
    logs = driver.get_log("performance")
    for log in logs:
        # Parse the log message
        message = json.loads(log['message'])
        # Check if the message contains geolocation information
        if 'geolocation' in str(message):
            print(message)  # Print the entire message for debugging
            # You may want to extract specific data from the message here

# Main loop to continuously get location
try:
    while True:
        get_location()
        time.sleep(300)  # Wait for 5 minutes
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    driver.quit()  # Close the browser instance when done