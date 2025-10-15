from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


# ===== Helper Functions =====
def safe_find(driver, by, value, retries=3, delay=3):
   for i in range(retries):
       try:
           element = driver.find_element(by, value)
           return element
       except:
           time.sleep(delay)
   return None


def wait_for_url(driver, url_contains, timeout=15):
   try:
       WebDriverWait(driver, timeout).until(EC.url_contains(url_contains))
   except:
       print(f"Timeout: URL did not contain '{url_contains}' within {timeout}s")


def take_screenshot(driver, name):
   driver.save_screenshot(name)


def click_safely(driver, element):
   try:
       driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
       time.sleep(random.uniform(1,2))
       element.click()
   except:
       try:
           driver.execute_script("arguments[0].click();", element)
       except Exception as e:
           print(f"Failed to click element: {e}")


def scroll_page(driver, times=3, delay_range=(1,2)):
   body = driver.find_element(By.TAG_NAME, "body")
   for i in range(times):
       body.send_keys(Keys.PAGE_DOWN)
       time.sleep(random.uniform(*delay_range))


# ===== Browser Setup =====
def start_browser():
   driver = webdriver.Chrome()
   driver.maximize_window()
   return driver


# ===== Main Flow =====
def main_flow(driver):
   base_url = "http://127.0.0.1:8000/"


   # --------- Homepage + Sections ---------
   driver.get(base_url)
   take_screenshot(driver, "homepage.png")
   scroll_page(driver, 2, (1,1))


   sections = {
       "transparency": "transparency.png",
       "citizen_power": "citizen_power.png",
       "government_power": "government_power.png"
   }
   for sec, shot in sections.items():
       try:
           driver.get(f"{base_url}about/#{sec}")
           wait_for_url(driver, sec)
           take_screenshot(driver, shot)
           scroll_page(driver, 2, (1,1))
       except:
           print(f"Failed to open {sec}")


   # --------- Registration ---------
   driver.get(f"{base_url}login/")
   wait_for_url(driver, "login")
   take_screenshot(driver, "login_page.png")


   register_link = safe_find(driver, By.LINK_TEXT, "Register") or \
                   safe_find(driver, By.XPATH, "//a[contains(text(),'Register')]")
   if register_link:
       click_safely(driver, register_link)
   wait_for_url(driver, "register")
   take_screenshot(driver, "register_page.png")


   user_data = {
       "username": "mijon",
       "first_name": "mijon",
       "last_name": "roza",
       "email": "mijon4533@gmail.com",
       "password1": "r",
       "password2": "r",
       "division": "Dhaka",
       "district": "Gazipur",
       "upazila": "Tongi"
   }


   for name, value in user_data.items():
       field = safe_find(driver, By.NAME, name)
       if field:
           field.clear()
           time.sleep(random.uniform(1, 2))
           field.send_keys(value)


   register_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Register')]")
   if register_btn:
       click_safely(driver, register_btn)
   wait_for_url(driver, "login")
   take_screenshot(driver, "after_register.png")


   # --------- Login ---------
   username = safe_find(driver, By.NAME, "username")
   password = safe_find(driver, By.NAME, "password")
   if username: username.send_keys("mijon")
   if password: password.send_keys("r")  # login password set to "r"
   login_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Login')]")
   if login_btn: click_safely(driver, login_btn)
   wait_for_url(driver, "dashboard")
   take_screenshot(driver, "dashboard.png")
   scroll_page(driver, 2, (1,1))


   # --------- Newsfeed Scroll + Interaction ---------
   driver.get(f"{base_url}list/")
   wait_for_url(driver, "list")
   scroll_page(driver, 3, (1,1))


   first_like_btn = safe_find(driver, By.XPATH, "(//button[contains(text(),'Like')])[1]")
   if first_like_btn: click_safely(driver, first_like_btn)


   first_comment_field = safe_find(driver, By.XPATH, "(//textarea[@placeholder='Add a comment'])[1]")
   if first_comment_field:
       first_comment_field.send_keys("Great post! 😊")
       first_comment_field.send_keys(Keys.ENTER)


   take_screenshot(driver, "newsfeed_interacted.png")


   # --------- Profile + NID Verification ---------
   profile_url = f"{base_url}profile/mijon/"
   driver.get(profile_url)
   wait_for_url(driver, "profile")
   take_screenshot(driver, "profile_before.png")
   scroll_page(driver, 1, (1,1))


   nid_field = safe_find(driver, By.NAME, "nid_number") or \
               safe_find(driver, By.XPATH, "//input[@placeholder='Enter your NID number']")
   if nid_field:
       nid_field.clear()
       nid_field.send_keys("1234567890")


   submit_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Submit for Verification')]")
   if submit_btn: click_safely(driver, submit_btn)
   take_screenshot(driver, "profile_after_verification.png")


   print("Automation complete ✅")


# ===== Close Browser =====
def close_browser(driver):
   driver.quit()


# ===== Run =====
if __name__ == "__main__":
   driver = start_browser()
   try:
       main_flow(driver)
   finally:
       close_browser(driver)




