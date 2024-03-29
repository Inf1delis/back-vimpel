import http.client

from bs4 import BeautifulSoup

import common.log as log
import variables

log.configure_logging(variables.YANDEX_WEATHER_LOGFILE)

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}


def weather_redirect_request():
    url = "/pogoda/irkutsk"
    for _ in range(3):
        conn = http.client.HTTPSConnection("yandex.ru")
        conn.request("GET", url, headers=HEADERS)
        response = conn.getresponse()
        if response.status not in (301, 302):
            return response
        url = response.getheader("Location")


def yandex_weather():
    try:
        response = weather_redirect_request()
        str_resp = response.read().decode("utf-8")
        soup = BeautifulSoup(str_resp, 'html.parser')
        # day = soup.find("div", class_="fact")
        #
        # data = {
        #     'date': soup.findAll("time", class_="forecast-briefly__date")[4].text,
        #     'temp_value': day.find('span', class_='temp__value').text,
        #     'condition_img': day.find('div', class_='link__condition').text.lower().replace(' ', '_') + '.svg',
        #     'wind': day.find('span', class_='wind-speed').text,
        #     'term_value': day.find('div', class_='fact__humidity').find('div', 'term__value')["aria-label"].split(':')[1].strip(),
        #     'feel_temp': day.find('div', class_='fact__feelings').find('span', class_='temp__value').text
        # }
        mydivs = soup.findAll("li", class_="forecast-briefly__day")

        data = []

        for day in mydivs[1:8]:
            temps = day.findAll('span', class_='temp__value')
            day_data = {
                'weekday': day.find("div", class_="forecast-briefly__name").text,
                'date': day.find("time").string,
                'condition_img': day.find("div", class_="forecast-briefly__condition").text.lower().replace(
                    ' ',
                    '_'
                ) + '.svg',
                'day_temp': temps[0].string.replace('−', '-'),
                'night_temp': temps[1].string.replace('−', '-')
            }

            data.append(day_data)
        log.logger.info("OK")
        return data
    except Exception as e:
        log.logger.exception(e)
        return "Error"


if __name__ == "__main__":
    print(yandex_weather())
