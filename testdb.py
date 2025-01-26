import mysql.connector

try:
    conn = mysql.connector.connect(
        host="VH301.spaceweb.ru",
        user="romablunt_infl",
        password="Samara2022",
        database="romablunt_infl",
        port=3306  # Указываем порт, если он отличается от стандартного
    )
except mysql.connector.Error as err:
    print("Не удалось подключиться к базе данных:", err)
else:
    print("Подключение успешно установлено!")