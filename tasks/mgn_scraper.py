import argparse
import requests
import platform
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

def start_driver():
    gecko_service = Service(GeckoDriverManager().install())
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    return webdriver.Firefox(service=gecko_service, options=firefox_options)

def get_images(dir_name, image_ids):
    filename = f"{dir_name}/credits.txt"
    
    # Load env variables
    load_dotenv()
    USERNAME = os.getenv("MGN_USERNAME")
    PASSWORD = os.getenv("MGN_PASSWORD")

    driver = start_driver()
    driver.get("https://new.mgnonline.com/")

    # Login
    login_btn = driver.find_element(By.LINK_TEXT, "log in")
    assert login_btn is not None
    print("Logging In")
    login_btn.click()
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    driver.find_element(By.ID, "btnLogin2").click()

    assert driver.find_element(By.LINK_TEXT, "log out") is not None
    print("Credentials accepted")

    main_tab = driver.current_window_handle

    # Loop through image ids
    for image_id in image_ids:
        print(f"\nScraping image {image_id}")
        current_url = driver.current_url
        search_bar = driver.find_element(By.ID, "searchTerm")
        search_bar.clear()
        search_bar.send_keys(image_id)
        search_bar.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(EC.url_changes(current_url))

        # If image details don't appear, click on the image after 2 seconds
        try:
            WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, "//div[contains(text(), 'Image Id: ')]"))
        except:
            driver.find_element(By.XPATH, "//ul[@id='og-grid']//li[2]").click()
            assert driver.find_element(By.XPATH, "//div[contains(text(), 'Image Id: ')]") is not None

        # Find image credit
        try:
            credit = driver.execute_script("""
                var creditSpan = document.querySelector('span.credit');
                if (creditSpan && creditSpan.nextSibling) {
                    return creditSpan.nextSibling.textContent.trim();
                }
                return '';
            """)            
            print(f"Found image credit: {credit}")
            with open(filename, "a") as f:
                f.write(f"{image_id}: {credit}\n")
        except Exception as e:
            print(f"Error finding image credit: {e}")
            with open(filename, "a") as f:
                f.write(f"{image_id}: Error finding credit\n")

        # Save Image
        print("Saving image")
        try:
            # Open image in new tab
            time.sleep(1)
            element = driver.find_element(By.CSS_SELECTOR, "i.fa.fa-file-image-o.mgntool[title='View File']")
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()

            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)

            # Download image
            image_element = driver.find_element(By.TAG_NAME, "img")
            image_src = image_element.get_attribute("src")

            # Convert the cookies to the format that the requests library expects
            cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

            # Set a User-Agent header to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            # Download the image
            response = requests.get(image_src, headers=headers, cookies=cookies)
            if response.status_code == 200:
                with open(f"{dir_name}/{image_id}.jpg", "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to download image, status code: {response.status_code}")

            # Close image tab
            driver.close()
            driver.switch_to.window(main_tab)
        except Exception as e:
            print(f"Error: {e}")
            driver.quit()
            exit()

    print(f"All images downloaded and can be found in: {dir_name}/")
    driver.quit()
        
if __name__ == '__main__':
    # Get cli arguments
    parser = argparse.ArgumentParser(description='Scrape MGN website')
    parser.add_argument('-l', '--list', help='List of image ids to scrape', type=str)

    args = parser.parse_args() 
    image_ids = [int(item) for item in args.list.split(",")]

    dir_name = f"batch_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.mkdir(dir_name)
    get_images(dir_name, image_ids)