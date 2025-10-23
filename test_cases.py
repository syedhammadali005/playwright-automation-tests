from playwright.sync_api import Page, TimeoutError
import time
import os

# ✅ Test Case 1: Login
def tc_login(page: Page, params: dict):
    try:
        print("➡ Starting login test...")
        page.goto(params["url"])
        page.fill("input[id='email']", params["email"])
        page.fill("input[id='password']", params["password"])
        page.click("button[type='submit']")
        page.wait_for_selector("text=Welcome", timeout=15000)
        print("✅ Login successful!")
        return "PASS"
    except TimeoutError:
        print("❌ Login failed! Timeout waiting for Welcome text.")
        os.makedirs("logs", exist_ok=True)
        page.screenshot(path="logs/login_fail.png")
        return "FAIL"
    except Exception as e:
        print(f"❌ Unexpected login error: {e}")
        return "FAIL"


# ✅ Test Case 2: Side Menu Navigation
def tc_side_menu(page: Page, params: dict):
    try:
        print("➡ Navigating side menu...")
        page.click("text=Application")
        time.sleep(1)
        page.click("text=Datasets")
        time.sleep(1)
        page.click("text=List")
        time.sleep(1)
        page.click("text=Analytics")
        time.sleep(1)
        page.click("text=Views")
        time.sleep(2)
        print("✅ Side menu navigation done!")
        return "PASS"
    except Exception as e:
        print(f"❌ Side menu failed! {e}")
        return "FAIL"


# ✅ Test Case 3: Create New List
def tc_create_list(page: Page, params: dict):
    """Creates a new List under Datasets section"""
    try:
        print("➡ Navigating to List section...")
        page.wait_for_selector("text=List", timeout=10000)
        page.click("text=List")
        page.wait_for_timeout(3000)

        # Click on Create button
        print("🧾 Clicking Create button...")
        page.wait_for_selector("button:has-text('Create')", timeout=10000)
        page.click("button:has-text('Create')")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(4000)

        # Try to find the List Name input with different selectors
        print("🔍 Searching for List Name field...")
        possible_selectors = [
            "input[placeholder*='List name']",
            "input[placeholder*='list name']",
            "input[placeholder*='List Name']",
            "input[placeholder*='* List name']",
            "input >> nth=0"
        ]

        found_selector = None
        for selector in possible_selectors:
            try:
                page.wait_for_selector(selector, timeout=5000)
                found_selector = selector
                break
            except:
                continue

        if not found_selector:
            os.makedirs("logs", exist_ok=True)
            page.screenshot(path="logs/list_popup_not_found.png")
            raise Exception("List creation form not found after clicking Create!")

        # Fill the form
        print(f"✅ Found List Name field using: {found_selector}")
        page.fill(found_selector, "Automation Test List")
        time.sleep(1)

        page.fill("input[placeholder*='Enter list title']", "Name")
        page.click("button:has-text('Add field')")
        page.fill("#create-list-form_list_1_title", "Contact No")
        page.click("button:has-text('Add field')")
        page.fill("#create-list-form_list_2_title", "Email")
        page.click("button:has-text('Add field')")
        page.fill("#create-list-form_list_3_title", "Address")
        page.click("button:has-text('Add field')")
        page.fill("#create-list-form_list_4_title", "Description")

        # Save list
        print("💾 Saving the list...")
        page.click("button:has-text('Save')")
        page.wait_for_timeout(4000)

        # Verify success message or new list appears
        # if page.is_visible("text=List created successfully") or page.is_visible("text=Automation Test List"):
        #     page.wait_for_timeout(4000)
        #     print("✅ List created successfully!")
        #     return "PASS"
        # else:
        #     os.makedirs("logs", exist_ok=True)
        #     page.screenshot(path="logs/list_save_maybe_failed.png")
        #     raise Exception("List Save button clicked but confirmation not visible.")

    except Exception as e:
        print(f"❌ List creation failed! {e}")
        os.makedirs("logs", exist_ok=True)
        page.screenshot(path="logs/list_creation_error.png")
        return "FAIL"
