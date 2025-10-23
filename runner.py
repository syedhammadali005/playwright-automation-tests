from playwright.sync_api import sync_playwright
import pandas as pd
import test_cases
import traceback
import os
from datetime import datetime

# Test Data
test_data = {
    "url": "https://snd-pakoxygen.kuickapp.com/",
    "email": "waseem.sajjad@pakoxygen.com",
    "password": "P@kistan01"
}

# Test Suite
test_suite = [
    {"id": "TC001", "name": "Login Test", "func": test_cases.tc_login},
    {"id": "TC002", "name": "Side Menu Test", "func": test_cases.tc_side_menu},
    {"id": "TC003", "name": "List Creation Test", "func": test_cases.tc_create_list},
]

results = []

# ensure logs folder exists
os.makedirs("logs", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    for test in test_suite:
        print(f"\n🚀 Running: {test['id']} - {test['name']}")
        test_folder = os.path.join("logs", f"{test['id']}_{test['name'].replace(' ', '_')}")
        os.makedirs(test_folder, exist_ok=True)

        try:
            status = test["func"](page, test_data)
            error_msg = ""
        except Exception as e:
            status = "FAIL"
            error_msg = str(e) + "\n" + traceback.format_exc()
            print(f"❌ {test['name']} failed with error: {e}")

            # take screenshot on failure
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(test_folder, f"fail_{timestamp}.png")
            page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            # optional error log file
            with open(os.path.join(test_folder, f"error_{timestamp}.txt"), "w", encoding="utf-8") as f:
                f.write(error_msg)

        results.append({
            "Test Case ID": test["id"],
            "Test Name": test["name"],
            "Status": status,
            "Error Log": error_msg
        })

    browser.close()

# Save results to Excel (append if exists)
output_file = "results.xlsx"
if os.path.exists(output_file):
    old_df = pd.read_excel(output_file)
    new_df = pd.DataFrame(results)
    df = pd.concat([old_df, new_df], ignore_index=True)
else:
    df = pd.DataFrame(results)

df.to_excel(output_file, index=False)
print("\n✅ Test results saved to results.xlsx!")
