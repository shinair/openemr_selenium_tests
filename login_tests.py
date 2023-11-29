import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from test_utils import *

class TestWebsite_login:
    @pytest.fixture(autouse=True)
    def login_page_setup(self):
        options = Options()
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        yield  # This allows the subsequent test methods to run
        self.browser.close()
        self.browser.quit()

    @pytest.mark.parametrize("url, username, password", read_configurations_from_file("secret.json"))
    def test_valid_admin_and_user_credentials(self, url, username, password):
        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys(username)
        self.browser.find_element(By.ID, "clearPass").send_keys(password)
        self.browser.find_element(By.ID, "login-button").submit()

        assert "https://in-info-web18.luddy.iupui.edu/interface/main/tabs/main.php" in self.browser.current_url

    @pytest.mark.parametrize("url", read_urls_from_file("secret.json"))
    def test_invalid_credentials(self, url):
        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys("abc")
        self.browser.find_element(By.ID, "clearPass").send_keys("abc")
        self.browser.find_element(By.ID, "login-button").submit()

        error_message_element = self.browser.find_element(By.CLASS_NAME,'bg-danger.text-light.py-2.px-3.login-failure.mb-3.font-weight-bold')
        assert error_message_element.is_displayed()
