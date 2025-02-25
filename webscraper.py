import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_emails_from_url_selenium(url):
    try:
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        
        time.sleep(3)  # Allow time for JavaScript to load
        
        text = driver.page_source  # Get full page source
        driver.quit()
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        
        return set(emails)  # Return unique emails
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

if __name__ == "__main__":
    url = input("Enter website URL: ")
    emails = extract_emails_from_url_selenium(url)
    
    if emails:
        print("Extracted Email Addresses:")
        for email in emails:
            print(email)
    else:
        print("No email addresses found.")
