from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
import mysql.connector



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
                            print(traceback.format_exc())  # Полная трассировка стека
                except Exception as e:
                    print("Ошибка при получении цены", e)
                    print(traceback.format_exc())  # Полная трассировка стека
    
    except Exception as e:
        print("Ошибка при работе с MySQL:", e)
        print(traceback.format_exc())  # Полная трассировка стека
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с MySQL закрыто")

def get_price(url):
    # Настройки для драйвера Chromium
    options = Options()
    options.headless = True  # Запускаем браузер в фоновом режиме (без графического интерфейса)
    #options.add_argument('--no-sandbox')  # Отключаем песочницу для повышения безопасности
    options.add_argument('--disable-dev-shm-usage')  # Отключение использования dev/shm для увеличения производительности

    # Указываем путь до исполняемого файла chromium
    driver = webdriver.Chrome(options=options, executable_path='/opt/chromium/chrome')

    try:
        # Открываем URL
        driver.get(url)
        print(f"URL открыт: {url}")  # Дополнительная точка логирования

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
        print(f"Произошла ошибка: {e}")
        print(traceback.format_exc())  # Полная трассировка стека
        return None
    finally:
        # Закрываем браузер
        driver.quit()

if __name__ == "__main__":
    main()