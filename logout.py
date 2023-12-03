import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from test_utils import *

class TestWebsite_logout:
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
    def test_logout(self, url, username, password):
        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys(username)
        self.browser.find_element(By.ID, "clearPass").send_keys(password)
        self.browser.find_element(By.ID, "login-button").submit()

        assert "https://in-info-web18.luddy.iupui.edu/interface/main/tabs/main.php" in self.browser.current_url

        # Close all open tabs first
        for tabClose in self.browser.find_elements(By.CSS_SELECTOR, 'span[class="fa fa-fw fa-xs fa-times"]'):
            tabClose.click()

        self.browser.find_element(By.ID, 'username').click()

        logout_element = self.browser.find_element(By.XPATH, '//li[@class="menuLabel"][last()]')
        logout_element.click()

        # Wait for the URL to change to the expected value
        expected_url = "https://in-info-web18.luddy.iupui.edu/interface/login/login.php?site=default"
        WebDriverWait(self.browser, 10).until(EC.url_to_be(expected_url))

        # Assert the current URL after logout
        assert self.browser.current_url == expected_url