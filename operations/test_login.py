import pytest
from selenium import webdriver
import allure


@pytest.fixture()
def test_setup():
    global driver
    #options = webdriver.FirefoxOptions()
    #webdriver = webdriver.Chrome()
    #driver = webdriver.Remote("selenium-hub.devops.svc.cluster.local:4444/wd/hub", options.to_capabilities())
    driver = webdriver.Chrome(executable_path="/home/devops/SELF/pytest-allure-selenium/chromedriver")
    # driver = webdriver.Remote("http://172.17.0.1:4444/wd/hub", options.to_capabilities()
    #driver = webdriver.Remote("selenium-hub.devops.svc.cluster.local:4444/wd/hub", options.to_capabilities())

    driver.implicitly_wait(10)
    driver.maximize_window();
    yield
    driver.quit()


@allure.description("Validate OrangeHRM with valid credentials")
@allure.severity(severity_level="CRITICAL")
def test_validLogin(test_setup):
    driver.get("https://orangehrm-demo-6x.orangehrmlive.com/");
    driver.find_element_by_id("txtUsername").clear();
    driver.find_element_by_id("txtPassword").clear();
    enter_username("admin");
    enter_password("admin123");
    log("Clicking Login Button")
    driver.find_element_by_id("btnLogin").click();
    assert "dashboard" in driver.current_url


@allure.description("Validate OrangeHRM with invalid credentials")
@allure.severity(severity_level="NORMAL")
def test_invalidLogin(test_setup):
    driver.get("https://orangehrm-demo-6x.orangehrmlive.com/");
    driver.find_element_by_id("txtUsername").clear();
    driver.find_element_by_id("txtPassword").clear();
    enter_username("admin");
    enter_password("admin123")
    log("Clicking login button")
    driver.find_element_by_id("btnLogin").click();
    try:
        assert "dashboard" in driver.current_url
    finally:
        if AssertionError:
            allure.attach(driver.get_screenshot_as_png(),
                          name="Invalid Credentials",
                          attachment_type=allure.attachment_type.PNG)


@allure.step("Entering Username as {0}")
def enter_username(username):
    driver.find_element_by_id("txtUsername").send_keys(username);


@allure.step("Entering Password as {0}")
def enter_password(password):
    driver.find_element_by_id("txtPassword").send_keys(password)


@allure.step("{0}")
def log(message):
    print(message)