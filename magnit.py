from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mysql.connector
import os

def main():
    try:
        # Подключение к базе данных
        print("Подключаюсь к базе")
        conn = mysql.connector.connect(
            host="VH301.spaceweb.ru",
            user="romablunt_infl",
            password="Samara2022",
            database="romablunt_infl"
        )
        print("Подключено к базе данных")  # Дополнительная точка логирования
        
        cursor = conn.cursor()
        
        # Запрос всех записей из таблицы links
        query = "SELECT id, product_id, distributor_id, url FROM links"
        cursor.execute(query)
        print("Выполнен запрос к таблице links")  # Дополнительная точка логирования
        
        for row in cursor.fetchall():
            id, product_id, distributor_id, url = row
            print(f"Обрабатываю URL: {url}")  # Дополнительная точка логирования
            

            query = "SELECT shop_id FROM shops where distributor_id=1"
            cursor.execute(query)
            print("Выполнен запрос к таблице shops")

            # Вызов функции для обработки каждого URL            
            
            for row1 in cursor.fetchall():
                try:
                    price = get_price(url+str(row1[0]))
                    if price: 
                        # SQL запрос для добавления записи в таблицу prices
                        insert_query = "INSERT INTO prices (product_id,price,shop_id) VALUES (%s, %s, %s)"
                        values = (product_id, price, row1[0])
                        
                        try:
                            cursor.execute(insert_query, values)
                            conn.commit()
                            print("Цена успешно добавлена в базу данных")  # Дополнительная точка логирования
                        except Exception as e:
                            print("Ошибка при добавлении цены:", e)
                            conn.rollback()
                except Exception as e:
                    print("Ошибка при получении цены", e)
    
    except Exception as e:
        print("Ошибка при работе с MySQL:", e)
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с MySQL закрыто")

def get_price(url):
    # Завершаем все запущенные процессы Chrome и ChromeDriver на Linux
    os.system("pkill -f chromedriver")
    os.system("pkill -f chrome")

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')  # Отключаем графический интерфейс

    # Оптимизация для Ubuntu Server
    chrome_options.add_argument('--remote-debugging-port=9222')  # Отладка
    chrome_options.add_argument('--disable-software-rasterizer')  # Отключаем софтверный рендеринг
    chrome_options.add_argument('--disable-extensions')  # Отключаем расширения
    chrome_options.add_argument('--disable-background-networking')  # Отключаем фоновые сетевые запросы
    chrome_options.add_argument('--disable-background-timer-throttling')  # Отключаем фоновые таймеры
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')  # Оптимизация для фоновых окон
    chrome_options.add_argument('--disable-breakpad')  # Отключаем crash-репорты
    chrome_options.add_argument('--disable-component-update')  # Отключаем обновления компонентов
    chrome_options.add_argument('--disable-default-apps')  # Отключаем стандартные приложения
    chrome_options.add_argument('--disable-domain-reliability')  # Отключаем сбор данных о доменах
    chrome_options.add_argument('--disable-features=AudioServiceOutOfProcess')  # Отключаем ненужные фичи
    chrome_options.add_argument('--disable-hang-monitor')  # Отключаем мониторинг зависаний
    chrome_options.add_argument('--disable-ipc-flooding-protection')  # Отключаем защиту от IPC-флуда
    chrome_options.add_argument('--disable-popup-blocking')  # Отключаем блокировку popup
    chrome_options.add_argument('--disable-prompt-on-repost')  # Отключаем запросы при повторной отправке форм
    chrome_options.add_argument('--disable-renderer-backgrounding')  # Отключаем фоновый рендеринг
    chrome_options.add_argument('--disable-sync')  # Отключаем синхронизацию
    chrome_options.add_argument('--force-color-profile=srgb')  # Используем стандартный цветовой профиль
    chrome_options.add_argument('--metrics-recording-only')  # Отключаем сбор метрик
    chrome_options.add_argument('--no-first-run')  # Пропускаем первый запуск
    chrome_options.add_argument('--safebrowsing-disable-auto-update')  # Отключаем обновления Safe Browsing
    chrome_options.add_argument('--enable-automation')  # Включаем режим автоматизации
    chrome_options.add_argument('--password-store=basic')  # Упрощаем хранение паролей
    chrome_options.add_argument('--use-mock-keychain')  # Используем mock keychain

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