from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Настраиваем headless режим
chrome_options = Options()
#chrome_options.add_argument("--headless")

# Инициализируем веб-драйвер
driver = webdriver.Chrome(options=chrome_options)

# Открываем нужный URL
url = "https://5ka.ru/product/3398823/batonchik-shokoladnyy-ye-g/"
driver.get(url)

# Ожидание загрузки элемента с ценой
# Ожидание загрузки элемента с ценой
price_container_xpath = '//div[@class="j_IdgaDq- css-k008qs"]'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, price_container_xpath)))

# Извлечение цены
price_parts = driver.find_elements(By.XPATH, '//div[@class="j_IdgaDq- css-k008qs"]//p')
price = f'{price_parts[0].text},{price_parts[1].text}'

print(f"Цена: {price}")
# Закрываем браузер
driver.quit()
