import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from test_utils import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestWebsite_vitals:
    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        options = Options()
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)

        yield
        self.browser.close()
        self.browser.quit()

    @pytest.mark.parametrize("url, username, password", read_configurations_from_file("secret.json"))
    def test_vitals_is_present_on_patient_dashboard(self, url, username, password):
        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys(username)
        self.browser.find_element(By.ID, "clearPass").send_keys(password)
        self.browser.find_element(By.ID, "login-button").submit()

        assert "https://in-info-web18.luddy.iupui.edu/interface/main/tabs/main.php" in self.browser.current_url

        # Close all open tabs first
        for tabClose in self.browser.find_elements(By.CSS_SELECTOR, 'span[class="fa fa-fw fa-xs fa-times"]'):
            tabClose.click()

        self.browser.find_element(By.ID, 'anySearchBox').send_keys('Abdul')
        self.browser.find_element(By.ID, 'search_globals').click()

        searchTable = self.browser.find_element(By.NAME, 'fin')
        assert searchTable is not None

        self.browser.implicitly_wait(5)

        iframe = self.browser.find_element(By.CSS_SELECTOR, '#framesDisplay > div > iframe')
        self.browser.switch_to.frame(iframe)

        patient1Found = self.browser.find_element(By.ID, "pid_1")

        patient1Found.click()

        self.browser.switch_to.default_content()

        iframe = self.browser.find_element(By.CSS_SELECTOR, '#framesDisplay > div > iframe')
        self.browser.switch_to.frame(iframe)

        container_div = self.browser.find_element(By.ID, 'container_div')

        main_divs = container_div.find_elements(By.CLASS_NAME, 'main.mb-5')

        for div in main_divs:
            try:
                class_row = div.find_element(By.CLASS_NAME, 'row')

                card_sections = class_row.find_elements(By.CSS_SELECTOR, 'section.card.mb-2')

                # If there are sections, interact with the last one
                if card_sections:
                    last_card_section = card_sections[-1]

                    vitals_expand_div = last_card_section.find_element(By.ID, 'vitals_ps_expand')
                    vitals_id = vitals_expand_div.find_element(By.ID, 'vitals')

                    span_text = vitals_expand_div.find_element(By.CLASS_NAME, 'text')

                    link_to_click = span_text.find_element(By.PARTIAL_LINK_TEXT,
                                                           'Click here to view and graph all vitals.')
                    link_to_click.click()

                    break
            except NoSuchElementException:
                pass














