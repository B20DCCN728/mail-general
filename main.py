import logging
import re
import time
from playwright.sync_api import sync_playwright, Page, expect, BrowserContext, BrowserType
from gmail import get_new_message
from file import get_data
import colorlog

# Set up logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s:%(levelname)s: %(message)s'
))

logger = logging.getLogger('ЧВК «Вагнер»')
logger.addHandler(handler)

# Set the log level to INFO
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    # Get email list
    email_list = get_data(r"C:\Users\Nguyen Hoang Viet\Documents\Accounts\Gmail\BAD2LJAVMB.txt")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=r"D:\Documents\Gologin_Profile\profile_6",
            headless=False,
            devtools=False,
            executable_path=r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-119\chrome.exe",
            args=[
                '--start-maximized',
                '-window-position=0,0',
                '--disable-blink-features=AutomationControlled'
            ]
        )

        page = browser.new_page()

        # Link
        page.goto("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail"
                  "%2Fu%2F0%2F&emr=1&flowEntry=ServiceLogin&flowName=GlifWebSignIn&followup=https%3A%2F%2"
                  "Fmail.google.com%2Fmail%2Fu%2F0%2F&hl=en&ifkv=ASKXGp1yrJnaigFg7h61ylkBGBSA-rERHwCoQ26UjUX_"
                  "9BrVfrhprfCvFfqD9KWIaoA5E7uNAEhRwA&osid=1&passive=1209600&service=mail&"
                  "theme=glif&dsh=S1108027641%3A1706621178643366"
                  )

        # Enter email
        page.get_by_label("Email or phone").fill(email_list[1]['email'])
        logger.info(f"Done filling email: {email_list[1]['email']}")
        time.sleep(2)

        # Click next button
        page.locator(
            'xpath=//*[@id="identifierNext"]/div/button'
        ).click()
        logger.info("Clicked next button")
        time.sleep(2)

        # Enter password
        page.get_by_label("Enter your password").fill(email_list[1]['password'])
        logger.info(f"Done filling password: {email_list[1]['password']}")
        time.sleep(2)

        # Click login
        page.locator(
            'xpath=//*[@id="passwordNext"]/div/button'
        ).click()
        logger.info("Clicked login button")
        time.sleep(5)

        # Click Now now button
        page.locator(
            'xpath=//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button'
        ).click()
        logger.info("Clicked Not now button")
        time.sleep(2)

        # Click Now now button
        page.locator(
            'xpath=//*[@id="yDmH0d"]/c-wiz[2]/div/div/div/div[2]/div[4]/div[1]/button'
        ).click()
        logger.info("Clicked Not now button")
        time.sleep(10)

        # Close browser
        browser.close()
