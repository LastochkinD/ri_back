from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys

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
    # Завершаем все запущенные процессы Chrome и ChromeDriver на Linux
    #os.system("pkill -f chromedriver")
    #os.system("pkill -f chrome")

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Отключаем графический интерфейс

    # Создание экземпляра драйвера Chrome
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Открываем URL
        driver.get(url)
        # Ожидаем загрузки элементов на странице
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "unit-footer-section-contacts")))
        
        # Получаем элемент по XPath
        price_element = driver.find_element(By.XPATH, '//meta[@itemprop="price"]')
        # Получаем значение атрибута content
        raw_price = price_element.get_attribute('content')

        # Возвращаем найденную цену
        return raw_price
    except Exception as e:
        print(f"Произошла ошибка при поиске цены на странице:")
        return None
    finally:
        # Закрываем браузер
        driver.quit()

if __name__ == "__main__":
    main()