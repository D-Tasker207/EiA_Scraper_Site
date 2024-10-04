import requests
import os
import time
import tempfile 
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

from app.socketio_handlers import Progress, send_error

def start_driver():
    gecko_service = Service(GeckoDriverManager().install())
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    return webdriver.Firefox(service=gecko_service, options=firefox_options)

def get_images(sid, image_ids):
    """
    Steps:
    1. Start driver
    2. Go to MGN website
    3. Login
    4. Loop through image ids
    4.1 Search for image id
    4.2 Find image credit
    4.3 Save image
    5. Close driver
    """

    # Set up progress
    total_steps = len(image_ids) * 2 + 4
    progress_tracker = Progress(sid, total_steps)

    temp_dir = tempfile.mkdtemp() 

    # Create credits file
    credit_file = f"{temp_dir}/credits.txt"
    
    # Load env variables
    load_dotenv()
    USERNAME = os.getenv("MGN_USERNAME")
    PASSWORD = os.getenv("MGN_PASSWORD")

    # Start driver
    progress_tracker.update("Starting driver")
    driver = start_driver()
    driver.get("https://new.mgnonline.com/")

    # Login
    progress_tracker.update("Logging in")
    login_btn = driver.find_element(By.LINK_TEXT, "log in")
    assert login_btn is not None
    login_btn.click()
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    driver.find_element(By.ID, "btnLogin2").click()

    assert driver.find_element(By.LINK_TEXT, "log out") is not None

    main_tab = driver.current_window_handle

    # Loop through image ids
    for i, image_id in enumerate(image_ids):
        progress_tracker.update(f"{i}/{len(image_ids)}: Finding image: {image_id}")
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
        progress_tracker.update(f"{i}/{len(image_ids)}: Saving image credit: {image_id}")
        try:
            credit = driver.execute_script("""
                var creditSpan = document.querySelector('span.credit');
                if (creditSpan && creditSpan.nextSibling) {
                    return creditSpan.nextSibling.textContent.trim();
                }
                return '';
            """)            
            with open(credit_file, "a") as f:
                f.write(f"{image_id}: {credit}\n")
        except Exception as e:
            send_error(f"{i}/{len(image_ids)}: Error finding image credit: {e}")
            with open(credit_file, "a") as f:
                f.write(f"{image_id}: Error finding credit\n")

        # Save Image
        progress_tracker.update(f"{i}/{len(image_ids)} Saving image")
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
                with open(f"{temp_dir}/{image_id}.jpg", "wb") as f:
                    f.write(response.content)
            else:
                send_error(f"{i}/{len(image_ids)}: Failed to download image, status code: {response.status_code}")

            # Close image tab
            driver.close()
            driver.switch_to.window(main_tab)
        except Exception as e:
            send_error(f"{i}/{len(image_ids)}: Error: {e}")
            driver.quit()
            exit()

    progress_tracker.update("Cleaning Up")
    driver.quit()

    return temp_dir