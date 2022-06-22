"""
import pytest
from selenium import webdriver
@pytest.fixture()
def setup():
    driver = webdriver.Chrome(executable_path="/home/ticvictech/PycharmProjects/Sixvercel_project/Drivers/chromedriver")
    return driver
"""
import os.path
from datetime import datetime

from selenium import webdriver
import pytest
from termcolor import colored
@pytest.fixture()
def setup(browser):
    global driver
    if browser=='chrome':
        driver=webdriver.Chrome(executable_path="/home/ticvictech/PycharmProjects/pythonProject2/Drivers/chromedriver")
        print("Launching Chrome browser")
    elif browser=='firefox':
        driver=webdriver.Firefox(executable_path="/home/ticvictech/PycharmProjects/nopcommerceProject/Drivers/geckodriver")
        print("Launching Firefox browser")
    else:
        driver = webdriver.Chrome(executable_path="/home/ticvictech/PycharmProjects/pythonProject2/Drivers/chromedriver")
    return driver
def pytest_addoption(parser): #This method is to select the browser in CLI (run time as argument)
    parser.addoption("--browser")

@pytest.fixture()
def browser(request):#return the browser value
    return request.config.getoption("--browser")

#htmlreport code
#it is hook for adding environment info into HTML report
def pytest_configure(config):
    config._metadata['Project Name']='Sixvercel'
    config._metadata['Module name']='RegisterwithLogin'
    config._metadata['Tester'] ='Manikandan'
#it is hook for delete/modyfy environment info into HTML report


@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("Javahome",None)
    metadata.pop("Plugins",None)
#these are customisable we can adding a command

#the above function for attach screen shots with the html report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url("https://nextjs-ecommerce-six.vercel.app/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory=os.path.dirname(item.config.option.htmlpath)
            file_name=report.nodeid.replace("::","_")+".png"
            destinationFile=os.path.join(report_directory,file_name)
            driver.save_screenshot(destinationFile)
            extra.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        report.extra = extra