#VH301.spaceweb.ru.
#romablunt_infl
#Samara2022
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

def get_price(url):
    # Настройки для драйвера Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Запускаем браузер в фоновом режиме (без графического интерфейса)
    driver = webdriver.Chrome(options=options)

    try:
        # Открываем URL
        driver.get(url)

        # Ждем пару секунд для загрузки элементов
        time.sleep(5)

        # Ожидаем загрузки элементов на странице
        wait = WebDriverWait(driver, 5)
        
        # Извлекаем элемент с ценой по атрибуту itemprop="price"
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, '//meta[@itemprop="price"]')))

        # Получаем значение атрибута content
        raw_price = price_element.get_attribute('content')

        # Возвращаем найденную цену
        return raw_price
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        # Закрываем браузер
        driver.quit()

# Пример использования
url = "https://magnit.ru/promo-product/2117434-maslo-slivochnoe-domik-v-derevne-krestyanskoe-725-180g?shopCode=630275"
price = get_price(url)
if price:
    print(f"Цена: {price}")  # Выводит цену в формате "рубли.копейки", например: "219.99"
else:
    print("Цена не найдена.")