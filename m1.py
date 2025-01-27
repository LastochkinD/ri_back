from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import traceback


def main():
    url = "https://magnit.ru/product/1000229091-pestravka_maslo_sliv_trad82_5_180g_fol_vitamilk_15?shopCode=996331"
    price = get_price(url)
    if price is not None:
        print(f"Цена товара: {price}")
    else:
        print("Не удалось получить цену.")


def get_price(url):
    # Настройки для драйвера Chromium
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Открываем URL
        driver.get(url)
        print(f"URL открыт: {url}")  # Дополнительная точка логирования

        # Ожидаем загрузки элементов на странице
        wait = WebDriverWait(driver, 10)  # Увеличим время ожидания до 10 секунд
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "unit-footer-section-contacts")))

        # Получаем элемент по XPath
        price_element = driver.find_element(By.XPATH, '//meta[@itemprop="price"]')
        # Получаем значение атрибута content
        raw_price = price_element.get_attribute('content')

        # Возвращаем найденную цену
        return raw_price
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print(traceback.format_exc())  # Полная трассировка стека
        return None
    finally:
        # Закрываем браузер
        driver.quit()


if __name__ == "__main__":
    main()