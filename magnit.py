from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import mysql.connector
import tempfile

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
    chrome_data_dir = tempfile.mkdtemp()
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Отключаем графический интерфейс
    chrome_options.add_argument("--disable-features=DBus")
    chrome_options.add_argument('--no-sandbox')  # Отключаем sandbox для работы без прав root
    chrome_options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью
    chrome_options.add_argument(f'--user-data-dir={chrome_data_dir}')  # Указываем уникальную ди
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
    except TimeoutException:
        print("Элемент не найден в течение отведенного времени.")
        return None
    except NoSuchElementException:
        print("Элемент с ценой не найден на странице.")
        return None
    except Exception as e:
        print(f"Произошла другая ошибка при поиске цены на странице: {e}")
        return None
    finally:
        # Закрываем браузер
        driver.quit()

if __name__ == "__main__":
    main()