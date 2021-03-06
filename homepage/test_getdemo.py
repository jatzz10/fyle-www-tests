import logging
import time

import pytest

from common.utils import resize_browser

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def browser(module_browser, base_url, request):
    resize_browser(browser=module_browser, resolution=request.param)
    time.sleep(0.5)
    module_browser.get(base_url)
    if module_browser.is_desktop():
        module_browser.click(xpath="//a[@id='best-expense-video-id']")
    else:
        module_browser.click(xpath="//div[contains(@class, 'sticky-cta-mobile')]/a")
    time.sleep(1)
    return module_browser

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        browser.input(xpath="//input[@name='email']", keys=email)
    if firstname:
        browser.input(xpath="//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//input[@name='lastname']", keys=lastname)
    if phone:
        browser.input(xpath="//input[@name='phone']", keys=phone)
    if company_size:
        browser.click(xpath="//input[@id='number_of_employees']")
        browser.click(xpath=f"//li[@data-value='{company_size}']")
    if agree:
        browser.click(xpath='//div[contains(@class, "custom-checkbox")]')
    browser.click(xpath='//button[text()="Get a demo"]')

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_bad_email(browser):
    submit_getdemo_form(browser, email='foo')
    e = browser.find(xpath="//label[@for='demo-email'][@class='error']")
    assert e and e.is_displayed(), 'No error displayed for invalid email'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_missing_firstname(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in')
    e = browser.find(xpath="//label[@for='demo-first-name'][@class='error demo-first-name-error']")
    assert e and e.is_displayed(), 'No error displayed for missing firstname'

@pytest.mark.parametrize('browser', [('desktop_1'), ('mobile_1')], indirect=True)
def test_success(browser):
    submit_getdemo_form(browser, email='megatron@fyle.in', firstname='Megatron', lastname='Transformer', phone='123456789', company_size='Under 5', agree=True)
    time.sleep(2)
    e = browser.find(xpath="//h3[contains(text(), 'Thank')]")
    assert e and e.is_displayed(), 'Not displaying thank you message'
