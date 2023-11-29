import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from test_utils import *

class TestWebsite_patient_search:
    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        options = Options()
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)

        yield  # This allows the subsequent test methods to run
        self.browser.close()
        self.browser.quit()

    @pytest.mark.parametrize("url, username, password", read_configurations_from_file("secret.json"))
    def test_search_found_patient_using_search_bar(self, url, username, password):
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
        assert patient1Found is not None

    @pytest.mark.parametrize("url, username, password", read_configurations_from_file("secret.json"))
    def test_search_not_found_patient_using_search_bar(self, url, username, password):

        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys(username)
        self.browser.find_element(By.ID, "clearPass").send_keys(password)
        self.browser.find_element(By.ID, "login-button").submit()

        assert "https://in-info-web18.luddy.iupui.edu/interface/main/tabs/main.php" in self.browser.current_url

        # Close all open tabs first
        for tabClose in self.browser.find_elements(By.CSS_SELECTOR, 'span[class="fa fa-fw fa-xs fa-times"]'):
            tabClose.click()

        self.browser.find_element(By.ID, 'anySearchBox').clear()
        self.browser.find_element(By.ID, 'anySearchBox').send_keys('Xyz')
        self.browser.find_element(By.ID, 'search_globals').click()

        searchTableFound = self.browser.find_element(By.NAME, 'fin')
        assert searchTableFound is not None

        iframe = self.browser.find_element(By.CSS_SELECTOR, '#framesDisplay > div > iframe')
        self.browser.switch_to.frame(iframe)

        assert not len(self.browser.find_elements(By.ID, "pid_1"))

    @pytest.mark.parametrize("url, username, password", read_configurations_from_file("secret.json"))
    def test_search_found_patient_using_finder(self, url, username, password):

        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys(username)
        self.browser.find_element(By.ID, "clearPass").send_keys(password)
        self.browser.find_element(By.ID, "login-button").submit()

        assert "https://in-info-web18.luddy.iupui.edu/interface/main/tabs/main.php" in self.browser.current_url

        # Close all open tabs first
        for tabClose in self.browser.find_elements(By.CSS_SELECTOR, 'span[class="fa fa-fw fa-xs fa-times"]'):
            tabClose.click()

        finder_element = self.browser.find_element(By.XPATH, '//div[@class="menuLabel px-1" and text()="Finder"]')
        finder_element.click()

        iframe = self.browser.find_element(By.CSS_SELECTOR, '#framesDisplay > div > iframe')
        self.browser.switch_to.frame(iframe)

        # Assuming you have located the input element using an appropriate selector
        search_box = self.browser.find_element(By.CLASS_NAME, 'form-control.search_init')

        self.browser.implicitly_wait(10)

        # Input text into the search box
        search_box.send_keys("Abdul")

        patient1Found = self.browser.find_element(By.ID, "pid_1")
        assert patient1Found is not None

    @pytest.mark.parametrize("url, username, password", read_configurations_from_file("secret.json"))
    def test_search_not_found_patient_using_finder(self, url, username, password):

        self.browser.get(url)

        self.browser.find_element(By.ID, 'authUser').send_keys(username)
        self.browser.find_element(By.ID, "clearPass").send_keys(password)
        self.browser.find_element(By.ID, "login-button").submit()

        assert "https://in-info-web18.luddy.iupui.edu/interface/main/tabs/main.php" in self.browser.current_url

        # Close all open tabs first
        for tabClose in self.browser.find_elements(By.CSS_SELECTOR, 'span[class="fa fa-fw fa-xs fa-times"]'):
            tabClose.click()

        finder_element = self.browser.find_element(By.XPATH, '//div[@class="menuLabel px-1" and text()="Finder"]')
        finder_element.click()

        iframe = self.browser.find_element(By.CSS_SELECTOR, '#framesDisplay > div > iframe')
        self.browser.switch_to.frame(iframe)

        # Assuming you have located the input element using an appropriate selector
        search_box = self.browser.find_element(By.CLASS_NAME, 'form-control.search_init')

        self.browser.implicitly_wait(10)

        # Input text into the search box
        search_box.send_keys("xyz")

        assert not len(self.browser.find_elements(By.ID, "pid_1"))














