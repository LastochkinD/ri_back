from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
    options.headless = True  # Запускаем браузер в фоновом режиме (без графического интерфейса)
    options.add_argument('--no-sandbox')  # Отключаем песочницу для повышения безопасности
    options.add_argument('--disable-dev-shm-usage')  # Отключение использования dev/shm для увеличения производительности

    # Указываем путь до исполняемого файла chromium
    driver = webdriver.Chrome(options=options, executable_path="/path/to/chromedriver")  # Укажите здесь путь к вашему chromedriver

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