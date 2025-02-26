import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

# Define keywords to focus on
KEYWORDS = ["researcher", "profile", "team", "biography"]  # Adjust based on needs

def setup_driver():
    """Sets up and returns a Selenium WebDriver for Safari."""
    driver = webdriver.Safari()
    return driver

def extract_emails_from_url_selenium(driver, url):
    """Fetches a webpage using Selenium and extracts email addresses."""
    try:
        driver.get(url)
        time.sleep(3)  # Allow time for JavaScript to load

        text = driver.page_source  # Get full page source
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)

        return set(emails)  # Return unique emails
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

def get_internal_links(driver, url, domain):
    """Finds internal links on a webpage, filtering by keywords."""
    internal_links = set()
    try:
        driver.get(url)
        time.sleep(3)  # Allow time for JavaScript to load

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and urlparse(href).netloc == domain:
                # Only add links that contain at least one of the keywords
                if any(keyword in href.lower() for keyword in KEYWORDS):
                    internal_links.add(href)

    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
    return internal_links

def crawl_website_selenium(start_url, max_pages=10, delay=2):
    """Crawls a website to find emails across multiple pages with keyword filtering."""
    driver = setup_driver()
    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = {start_url}
    found_emails = set()

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
        print(f"Crawling: {url}")
        visited.add(url)

        emails = extract_emails_from_url_selenium(driver, url)
        found_emails.update(emails)

        internal_links = get_internal_links(driver, url, domain)
        to_visit.update(internal_links - visited)

        time.sleep(delay)  # Delay between requests

    driver.quit()
    return found_emails

def format_url(url):
    """Ensures the URL has a proper scheme (http/https)."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Default to https
    return url

if __name__ == "__main__":
    url = input("Enter website URL: ").strip()
    url = format_url(url)  # Ensure proper formatting
    emails = crawl_website_selenium(url, max_pages=20, delay=1)  # Increased pages

    if emails:
        print("\nExtracted Email Addresses:")
        for email in emails:
            print(email)
    else:
        print("\nNo email addresses found.")
