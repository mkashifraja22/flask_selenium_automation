from datetime import time
import time
from flask import Flask
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

app = Flask(__name__)


@app.route('/')
def start():  # put application's code here
    driver_path = ChromeDriverManager().install()

    try:
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        )
        # options.add_argument("__remote-allow-origins=*")

        # options.binary_location = 'chromedriver'
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        # disable images
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        headless_option = True

        if headless_option:
            # If headless mode enabled (eg for server), enable headless functions and virtual display
            # options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("start-maximized")
            options.add_argument("disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--incognito")

        proxy_options = None
        # if config.REQ_PROXY:
        #     proxy_options = {
        #         "proxy": {
        #             "http": config.REQ_PROXY,
        #             "https": config.REQ_PROXY,
        #             "no_proxy": "localhost,127.0.0.1",
        #         }
        #     }
        # print(self.driver_path, "driver path")

        if driver_path == "":
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Chrome(options=options)

        # Disable automation identities
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.set_window_size(1250, 1080)  # Upscale window
        driver.get("https://glvar.clareityiam.net/idp/login")
        print(driver.title)
        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        username.send_keys('username')
        password.send_keys('password')
        login_button = driver.find_element(By.ID, 'loginbtn')
        login_button.send_keys(Keys.ENTER)
        # try:
        # element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "panel1"))
        # )
        # # matrix = element.find_element(By.)
        # div_element = driver.find_element(By.CSS_SELECTOR, 'div[data-title="Matrix"]')
        # div_element.click()
        # time.sleep(10)
        # print("try")
        try:
            # driver.switch_to.window(driver.window_handles[1])

            driver.get("https://las.mlsmatrix.com/Matrix/Search/Residential")

            select_none = driver.find_element(By.ID, "S_MultiStatus_Select_None")
            a_tag = select_none.find_element(By.TAG_NAME, 'a')
            a_tag.click()

            label_element = driver.find_element(By.XPATH, '//label[text()="Expired"]')
            # Find the corresponding <input> element (checkbox)
            checkbox_element = label_element.find_element(By.XPATH, './preceding-sibling::input[@type="checkbox"]')
            # Check the checkbox
            if not checkbox_element.is_selected():
                checkbox_element.click()

            date_range = label_element.find_element(By.XPATH, '../../following-sibling::td/input[@type="text"]')
            date_range.clear()
            date_range.send_keys('0-2')

            price_label_element = driver.find_element(By.XPATH, '//span[contains(text(), "Price")]')
            price = price_label_element.find_element(By.XPATH, './following-sibling::input[@type="text"]')
            price.send_keys('249+')

            year_built_label_element = driver.find_element(By.XPATH, '//span[contains(text(), "Year Built")]')
            year_built = year_built_label_element.find_element(By.XPATH, './following-sibling::input[@type="text"]')
            year_built.send_keys('2021-')
            select_element = Select(driver.find_element(By.XPATH, '//select[@data-mtx-track="County"]'))
            select_element.select_by_visible_text("Clark County")

            result_button_element = driver.find_element(By.ID ,"m_ucSearchButtons_m_lbSearch")
            result_button_element.click()
            #
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "m_liSaveAsTab"))
                )
                # all_leads = driver.find_element(By.NAME ,"CHB_")
                # all_leads.click()

                leads_checkbox_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//input[@title="Check/Uncheck All on Page"]'))
                )

                # Click the checkbox to select it
                leads_checkbox_element.click()

                save_button_element = driver.find_element(By.ID, "m_liSaveAsTab")
                save_button_element.click()

                auto_email_button_element = driver.find_element(By.ID, "m_lbSaveAsAutoEmail")
                auto_email_button_element.click()
                # To add new contact
                # new_contact_element = driver.find_element(By.ID, "m_ucAutoEmailContact_m_lnkAdd")
                # new_contact_element.click()
                #
                # driver.switch_to.window(driver.window_handles[1])
                # label_element = driver.find_element(By.XPATH, '//label[text()="Expired"]')
                # checkbox_element = label_element.find_element(By.XPATH, './preceding-sibling::input[@type="checkbox"]')
                # # Check the checkbox
                # if not checkbox_element.is_selected():
                #     checkbox_element.click()
                #
                # Enable Reverse Prospecting

                select_element = Select(driver.find_element(By.ID, 'm_ucAutoEmailContact_m_ddlContacts'))
                select_element.select_by_visible_text("expired, test")

                label_element = driver.find_element(By.XPATH, '//label[text()="BCC me a copy of all emails"]')
                # Find the corresponding <input> element (checkbox)
                checkbox_element = label_element.find_element(By.XPATH, './preceding-sibling::input[@type="checkbox"]')
                if checkbox_element.is_selected():
                    checkbox_element.click()

                subject_input_element = driver.find_element(By.ID ,"m_txtSubject")
                subject_input_element.clear()
                subject_input_element.send_keys("Expired Leads from Automation")

                radio_button_element = driver.find_element(By.ID,"m_rbASAP")

                # Click the radio button to select it
                radio_button_element.click()

                final_save_button_element = driver.find_element(By.ID, "m_lnkSaveAutoEmail")
                final_save_button_element.click()

                # m_lnkSaveAutoEmail




            except Exception as e:
                print('eception called',e)


            # ml = driver.find_element(By.NAME, 'Fm9_Ctrl12_TextBox')
            # ml.send_keys("heloooo")
            time.sleep(10)
        finally:
            print("fist finaly")
            driver.quit()

        time.sleep(10)

        return "Selenum"
    except Exception as e:
        print(e)
        return "failed"


if __name__ == '__main__':
    app.run(debug=True)
