# govt_user.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import random


# ================= Helper Functions =================
def safe_find(driver, by, value, retries=3, delay=2):
    """Try to find an element safely with retries"""
    for i in range(retries):
        try:
            element = driver.find_element(by, value)
            print(f"Element found: {value}")
            return element
        except:
            print(f"Element not found: {value}, retry {i+1}/{retries}")
            time.sleep(delay)
    return None


def wait_for_url(driver, url_contains, timeout=15):
    """Wait until URL contains a substring"""
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(url_contains))
        print(f"URL contains '{url_contains}'")
    except:
        print(f"Timeout: URL did not contain '{url_contains}' in {timeout}s")


def click_safely(driver, element):
    """Safely click an element, using JS fallback if needed"""
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(random.uniform(1, 2))
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)
        print("Used JS click as fallback")


def human_typing(element, text):
    """Human-like typing"""
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def human_clear_and_type(element, text):
    """Backspace old text, then type new text"""
    old_text = element.get_attribute('value')
    for _ in range(len(old_text)):
        element.send_keys("\b")
        time.sleep(random.uniform(0.05, 0.12))
    human_typing(element, text)


# ================= Browser Setup =================
def start_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


# ================= Login =================
def login_govt(driver, username, password):
    driver.get("http://127.0.0.1:8000/login/")
    username_input = safe_find(driver, By.NAME, "username")
    password_input = safe_find(driver, By.NAME, "password")
    login_btn = safe_find(driver, By.XPATH, "//button[text()='Login']")

    if username_input and password_input:
        human_typing(username_input, username)
        human_typing(password_input, password)

    if login_btn:
        click_safely(driver, login_btn)

    wait_for_url(driver, "dashboard")
    print("Logged in as government user")


# ================= Approve Multiple Users on Dashboard =================
def approve_waiting_users(driver):
    driver.get("http://127.0.0.1:8000/dashboard/")
    wait_for_url(driver, "dashboard")
    time.sleep(2)

    while True:
        approve_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Approve')]")
        if not approve_buttons:
            print("No more awaiting verification users found.")
            break
        for i, btn in enumerate(approve_buttons):
            click_safely(driver, btn)
            print(f"Approved awaiting verification user #{i+1}")
            time.sleep(random.uniform(1,2))
        time.sleep(1)


# ================= Update Issue (Pending → In Progress → Resolved) =================
def approve_and_resolve_issue(driver):
    driver.get("http://127.0.0.1:8000/list/")
    wait_for_url(driver, "list")
    time.sleep(2)

    approve_btns = driver.find_elements(By.XPATH, "//button[contains(text(),'Approve')]")
    for btn in approve_btns:
        click_safely(driver, btn)
        print("Approved an issue")
        time.sleep(1)

    select_elem = safe_find(driver, By.XPATH, "//select")
    if select_elem:
        click_safely(driver, select_elem)
        time.sleep(random.uniform(0.5,1.5))
        status_text = select_elem.get_attribute('value').strip().lower()
        new_status = "In Progress" if status_text == "pending" else "Resolved"
        option_elem = select_elem.find_element(By.XPATH, f".//option[text()='{new_status}']")
        click_safely(driver, option_elem)
        print(f"Selected '{new_status}' status (human-like)")

        update_btn = safe_find(driver, By.XPATH, "//button[text()='Update']")
        if update_btn:
            click_safely(driver, update_btn)
            print("Clicked Update, waiting for notification...")
            try:
                notif = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[contains(text(),'Issue status updated') or contains(text(),'updated')]"))
                )
                print("Notification appeared:", notif.text)
            except:
                print("Notification not found or timeout.")


# ================= Create Poll =================
def create_poll(driver, question, options):
    driver.get("http://127.0.0.1:8000/polls/")
    wait_for_url(driver, "polls")
    time.sleep(2)

    create_btn = safe_find(driver, By.XPATH, "//a[contains(text(),'Create Poll')] | //button[contains(text(),'Create Poll')]")
    if create_btn:
        click_safely(driver, create_btn)
        time.sleep(2)

    question_input = safe_find(driver, By.NAME, "question")
    if question_input:
        human_typing(question_input, question)

    for i,opt in enumerate(options):
        option_input = safe_find(driver, By.NAME, f"option{i+1}")
        if option_input:
            human_typing(option_input, opt)
            time.sleep(random.uniform(0.2,0.5))

    submit_btn = safe_find(driver, By.XPATH, "//button[@type='submit' or contains(text(),'Submit')]")
    if submit_btn:
        click_safely(driver, submit_btn)
        print("Poll created successfully")
        time.sleep(2)


# ================= Scroll, Edit & Delete Poll =================
def edit_and_delete_poll(driver):
    driver.get("http://127.0.0.1:8000/polls/")
    wait_for_url(driver, "polls")
    time.sleep(2)

    # Scroll down to last poll to see human-like
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Scroll up to top and select first poll to edit
    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)
    edit_btn = safe_find(driver, By.XPATH, "(//a[contains(text(),'Edit')])[1]")
    if edit_btn:
        click_safely(driver, edit_btn)
        time.sleep(2)

        question_input = safe_find(driver, By.NAME, "question")
        if question_input:
            human_clear_and_type(question_input, "Updated question by govt user")

        for i, opt_name in enumerate(["Yes updated", "No updated", "Maybe updated", "Not Sure updated"]):
            option_input = safe_find(driver, By.NAME, f"option{i+1}")
            if option_input:
                human_clear_and_type(option_input, opt_name)
                time.sleep(random.uniform(0.2,0.5))

        save_btn = safe_find(driver, By.XPATH, "//button[@type='submit' or contains(text(),'Submit')]")
        if save_btn:
            click_safely(driver, save_btn)
            print("Edited poll successfully")
            time.sleep(2)

    delete_btn = safe_find(driver, By.XPATH, "(//a[contains(text(),'Delete')])[1]")
    if delete_btn:
        click_safely(driver, delete_btn)
        print("Deleted poll successfully")
        time.sleep(2)


# ================= Scroll Newsfeed =================
def scroll_newsfeed(driver):
    try:
        driver.get("http://127.0.0.1:8000/newsfeed/")
        wait_for_url(driver, "newsfeed")
        time.sleep(2)

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1.5,2.5))
        # Scroll up
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(random.uniform(1,2))
        print("Scrolled newsfeed down and up (human-like)")
    except Exception as e:
        print("Newsfeed scroll failed:", e)


# ================= Main Flow =================
if __name__ == "__main__":
    driver = start_browser()
    try:
        GOVT_USERNAME = "roza"
        GOVT_PASSWORD = "Afsara00"

        login_govt(driver, GOVT_USERNAME, GOVT_PASSWORD)
        time.sleep(2)

        approve_waiting_users(driver)
        time.sleep(2)

        approve_and_resolve_issue(driver)
        time.sleep(2)

        scroll_newsfeed(driver)
        time.sleep(2)

        create_poll(driver, "Should public services be increased?", ["Yes", "No", "Maybe", "Not Sure"])
        time.sleep(2)

        edit_and_delete_poll(driver)

        print("Automation complete successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        time.sleep(3)
        driver.quit()
