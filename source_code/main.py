from pyowm import OWM
from win11toast import toast
import time
import json
import pystray
import PIL.Image
import threading
import os
import webbrowser

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_weather_data(place, country, unit_of_measurement, api_key):
    try:
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(f"{place}, {country}")
        w = observation.weather
        temp = w.temperature(unit_of_measurement)['temp']
        result = str(round(temp))
        return result
    except Exception as e:
        print("Ошибка при получении данных о погоде:", e)
        raise

def show_weather_notification(place, country, title, content, unit_of_measurement, api_key):
    try:
        result = get_weather_data(place, country, unit_of_measurement, api_key)
        toast(title, f"{content} {result} °C", button='Закрыть')
    except Exception as e:
        print("Ошибка при показе уведомления о погоде:", e)
        raise

def close(icon):
    print("Программа завершена")
    icon.stop()

def config():
    os.startfile('data.json')

def github_open():
    webbrowser.open_new_tab("https://github.com/shashzxc/Weather-Notification-11")

def weather_thread(place, country, title, content, unit_of_measurement, delay, api_key, icon):
    while True:
        try:
            show_weather_notification(place, country, title, content, unit_of_measurement, api_key)
            time.sleep(delay)
        except Exception as e:
            print("Общая ошибка:", e)
            toast(f'Общая ошибка: {str(e)}, Программа остановит работу', button='Закрыть')
            icon.stop()
            break

def main():
    json_file_path = 'data.json'
    try:
        data = load_data_from_json(json_file_path)

        place = data['place']
        country = data['country']
        delay = int(data['delay'])
        title = data['title']
        content = data['content']
        unit_of_measurement = data['unit of measurement']
        api_key = data['api_key']

        image = PIL.Image.open("icon.png")
        icon = pystray.Icon('Weather Notification 11', image, menu=pystray.Menu(
            pystray.MenuItem('Узнать погоду сейчас',
                             lambda: show_weather_notification(place, country, title, content,
                                                              unit_of_measurement, api_key)),
            pystray.MenuItem('Открыть конфиг-файл', config),
            pystray.MenuItem('Открыть проект на Github', github_open),
            pystray.MenuItem('Закрыть', close)
        ))

        t = threading.Thread(target=weather_thread,
                             args=(place, country, title, content, unit_of_measurement, delay, api_key, icon))
        t.daemon = True
        t.start()

        icon.run()
    except Exception as e:
        print("Общая ошибка:", e)
        raise

if __name__ == '__main__':
    main()
