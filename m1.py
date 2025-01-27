from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Настройка опций Chrome для headless режима
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  # Этот параметр отключает графический интерфейс браузера

# Создание экземпляра драйвера Chrome
driver = webdriver.Chrome(options=chrome_options)

# Открытие URL
url = 'https://magnit.ru/product/1000229091-pestravka_maslo_sliv_trad82_5_180g_fol_vitamilk_15?shopCode=996331'
driver.get(url)

# Закрываем браузер после завершения работы
driver.quit()