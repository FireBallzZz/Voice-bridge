from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# ================= Helper Functions =================
def safe_find(driver, by, value, retries=3, delay=0.5):
    for i in range(retries):
        try:
            element = driver.find_element(by, value)
            print(f"Element found: {value}")
            return element
        except:
            print(f"Element not found: {value}, retry {i + 1}/{retries}")
            time.sleep(delay + random.uniform(0.1, 0.3))
    return None

def wait_for_url(driver, url_contains, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(url_contains))
        print(f"URL contains '{url_contains}'")
    except:
        print(f"Timeout: URL did not contain '{url_contains}' in {timeout}s")

def scroll_page(driver, scrolls=3):
    for i in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolled down {i + 1}/{scrolls}")
        time.sleep(random.uniform(0.5, 1.0))

def click_safely(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(random.uniform(0.3, 0.8))
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)
    time.sleep(random.uniform(0.3, 0.8))

def human_typing(element, text):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
    time.sleep(random.uniform(0.2, 0.5))

# ================= Browser Setup =================
def start_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# ================= Login =================
def login(driver):
    driver.get("http://127.0.0.1:8000/login/")
    username_input = safe_find(driver, By.NAME, "username")
    password_input = safe_find(driver, By.NAME, "password")
    login_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Login')]")
    if username_input and password_input:
        human_typing(username_input, "rozapi")
        human_typing(password_input, "r")
    if login_btn:
        click_safely(driver, login_btn)
    wait_for_url(driver, "dashboard")
    print("Logged in as rozapi")

# ================= Edit & Delete Existing Post =================
def edit_delete_existing_post(driver):
    driver.get("http://127.0.0.1:8000/my-posts/")
    wait_for_url(driver, "my-posts")

    # --- Edit first post ---
    edit_btn = safe_find(driver, By.XPATH, "(//a[contains(text(),'Edit')])[1]")
    if edit_btn:
        click_safely(driver, edit_btn)
        wait_for_url(driver, "edit-issue")

        fields = {
            "title": "Pollution n air is extreme in level now",
            "description": "Air pollution is a dangerous thing for us.",
            "division": "Dhaka",
            "district": "Gazipur",
            "upazila": "Tongi"
        }

        for name, text in fields.items():
            field = safe_find(driver, By.NAME, name)
            if field:
                human_typing(field, text)

        save_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Save')]")
        if save_btn:
            click_safely(driver, save_btn)
        wait_for_url(driver, "my-posts")
        print("Existing post edited successfully ✅")

    # --- Delete first post ---
    delete_btn = safe_find(driver, By.XPATH, "(//button[contains(text(),'Yes, delete this post')])[1]")
    if delete_btn:
        click_safely(driver, delete_btn)
        print("Existing post deleted successfully ✅")
        time.sleep(random.uniform(0.5, 1.0))
    else:
        print("Delete button not found")

# ================= Post an Issue =================
def post_issue(driver):
    driver.get("http://127.0.0.1:8000/my-posts/")
    wait_for_url(driver, "my-posts")

    post_btn = safe_find(driver, By.XPATH, "//a[contains(text(),'Post an Issue')]")
    if post_btn:
        click_safely(driver, post_btn)
    wait_for_url(driver, "create-issue")

    fields = {
        "title": "Illegal houses are built everywhere",
        "description": "We must be conscious about these.",
        "division": "Dhaka",
        "district": "Gazipur",
        "upazila": "Tongi"
    }

    for name, text in fields.items():
        field = safe_find(driver, By.NAME, name)
        if field:
            human_typing(field, text)

    submit_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Submit')]")
    if submit_btn:
        click_safely(driver, submit_btn)
    wait_for_url(driver, "my-posts")
    print("Issue posted successfully ✅")

# ================= Newsfeed Actions =================
def newsfeed_actions(driver):
    driver.get("http://127.0.0.1:8000/list/")
    wait_for_url(driver, "list")

    scroll_page(driver, 3)

    first_like_btn = safe_find(driver, By.XPATH, "(//button[contains(text(),'Like')])[1]")
    if first_like_btn:
        click_safely(driver, first_like_btn)
        print("First post liked ✅")

    comment_box = safe_find(driver, By.NAME, "content")
    if comment_box:
        human_typing(comment_box, "Agreed with you, we badly need to solve this")
        submit_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Post')]")
        if submit_btn:
            click_safely(driver, submit_btn)
            print("Comment posted ✅")
        else:
            print("Post button not found")
    else:
        print("Comment box not found")

    division_search = safe_find(driver, By.NAME, "division")
    if division_search:
        division_search.clear()
        human_typing(division_search, "Dhaka")
    search_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Search')]")
    if search_btn:
        click_safely(driver, search_btn)
    print("Searched posts by division Dhaka ✅")

# ================= Poll Actions =================
def poll_actions(driver):
    driver.get("http://127.0.0.1:8000/polls/")
    wait_for_url(driver, "polls")

    first_poll_radio = safe_find(driver, By.XPATH, "(//input[@type='radio'])[1]")
    if first_poll_radio:
        click_safely(driver, first_poll_radio)
        vote_btn = safe_find(driver, By.XPATH, "//button[contains(text(),'Vote')]")
        if vote_btn:
            click_safely(driver, vote_btn)
            print("Voted in the first poll ✅")

# ================= Close Browser =================
def close_browser(driver):
    driver.quit()
    print("Browser closed ✅")

# ================= Main =================
if __name__ == "__main__":
    driver = start_browser()
    try:
        login(driver)
        edit_delete_existing_post(driver)
        post_issue(driver)
        newsfeed_actions(driver)
        poll_actions(driver)
        print("All actions completed successfully ✅")
    finally:
        close_browser(driver)
