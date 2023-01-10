import json

import mpu
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def main():
    data = []
    options = Options()
    options.add_argument('--headless')

    url = 'https://api.exchangerate.host/latest'
    params = "?base=USD"

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url + params)

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))
    search = driver.find_element(by=By.TAG_NAME, value='pre')
    data.append(search.text)

    driver.quit()
    return data


data = main()
if data:
    json_format = json.loads(data[0])
    if json_format['success']:
        for key, value in json_format.items():
            print(key, value)
    list_name_of_code = []
    list_code_not_found = []
    for item in json_format['rates'].keys():
        try:
            list_name_of_code.append(mpu.units.get_currency(item))
        except Exception as e:
            list_code_not_found.append((item, {"error": e}))

    print(list_name_of_code)
    print(list_code_not_found)
