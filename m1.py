from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import tempfile

sys.stdout = open('log.txt', 'a')
sys.stderr = sys.stdout

def main():
    url = 'https://magnit.ru/product/1000229091-pestravka_maslo_sliv_trad82_5_180g_fol_vitamilk_15?shopCode=996331'
    try:
        price = get_price(url)
        print(f"Цена успешно добавлена в базу данных: {price}")
    except Exception as e:
        print("Ошибка при работе с MySQL:", e)

def get_price(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    # Создаем уникальную временную директорию для пользовательских данных
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "unit-footer-section-contacts")))
        price_element = driver.find_element(By.XPATH, '//meta[@itemprop="price"]')
        raw_price = price_element.get_attribute('content')
        return raw_price
    except Exception as e:
        print(f"Произошла ошибка при поиске цены на странице:")
        return None
    finally:
        driver.quit()
        # Удаляем временную директорию после завершения работы
        os.rmdir(user_data_dir)

if __name__ == "__main__":
    main()