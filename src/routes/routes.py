import routes.history_volume as history_volume
import routes.redirect_to_telegram as redirect_to_telegram
import routes.today_volume as today_volume
import routes.today_weather as today_weather

routes_list = [
    ['/today_weather', today_weather.today_weather, ['GET']],
    ['/redirection_to_telegram', redirect_to_telegram.redirection_to_telegram, ['POST', 'GET']],
    ['/today_volume', today_volume.today_volume, ['GET']],
    ['/history_volume', history_volume.history_volume, ['GET']]
]
