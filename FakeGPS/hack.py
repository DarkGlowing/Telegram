from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Настройки для Chrome
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")

driver = webdriver.Chrome(options=chrome_options)

# Функция для изменения геолокации
def change_geolocation(lat, lon):
    driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
        'latitude': lat,
        'longitude': lon,
        'accuracy': 100
    })

# Список геолокаций для смены
locations = [
    (37.7749, -122.4194),  # Сан-Франциско
    (34.0522, -118.2437),  # Лос-Анджелес
    (40.7128, -74.0060),   # Нью-Йорк
]

# Открытие страницы
driver.get("https://yandex.ru/maps")

try:
    while True:
        for lat, lon in locations:
            change_geolocation(lat, lon)
            print(f"Изменение геолокации на: {lat}, {lon}")
            time.sleep(0.5)  # Ждать 0.5 секунд
except KeyboardInterrupt:
    print("Скрипт остановлен.")

# Закрытие браузера
driver.quit()