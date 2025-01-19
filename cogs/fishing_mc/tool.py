from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import asyncio

async def send_code(gmail:str) -> None:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options)
        driver.get('https://www.microsoft.com/cascadeauth/store/account/signin?ru=https%3A%2F%2Fwww.microsoft.com%2Fja-jp%2Fmicrosoft-365%2Fbuy%2Fcompare-all-microsoft-365-products%3Ficid%3Dmscom_marcom_H1a_Microsoft365AI')
        username_field = driver.find_element(By.ID, 'i0116')
        button = driver.find_element(By.ID, 'idSIButton9')
        username_field.send_keys(gmail)
        button.click()
        await asyncio.sleep(5)
    except NoSuchElementException:
        return
    finally:
        driver.close()
    print('Succesfully to send code!')

if __name__ == '__main__':
    asyncio.run(send_code('example@gmail.com'))