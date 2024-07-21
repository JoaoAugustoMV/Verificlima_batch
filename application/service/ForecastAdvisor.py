import os, httpx, logging, json
from datetime import date, datetime, timedelta
from application.models.InformationDayForecast import InformationDayForecast
from application.service.WeatherForecastBase import WeatherForecastBase
# from application.repository.Repository import InfoRepository
# infoRepo = InfoRepository()

class ClimaAdvisorService(WeatherForecastBase):
    def __init__(self) -> None:
        self.source = 'APIADVISOR'
        self.city = 'SAO PAULO'

    async def __get_prediction_minus_x(self, x_days):
        current_date = datetime.now()
        data_mais_x = current_date + timedelta(days=x_days)
        data_key = data_mais_x.strftime('%Y-%m-%d')
        json = await self.__request_forecast()
        for dia_info in json['data']:
            if dia_info['date'] == data_key:
                dici = {
                        'cd_dia': int(data_key.replace('-', '')),
                        'x_dias': x_days,                        
                        'fonte': self.source,
                        'cidade': self.city
                    }
                if x_days == 0:
                    dici.update({
                        f'temperatura_real_min': dia_info['temperature']['min'],
                        f'temperatura_real_max':  dia_info['temperature']['max'], 
                    })
                else: 
                    dici.update({
                        f'dia_previsao_feita_menos_x': str(current_date.date()),
                        f'temperatura_min_previsao_feita_menos_x': dia_info['temperature']['min'],
                        f'temperatura_max_previsao_feita_menos_x':  dia_info['temperature']['max'],
                    })                
                return InformationDayForecast(**dici)
        
        return None
    
    async def __request_forecast(self):
        url = os.getenv("urlAdvisor")
        url = f'{url}/forecast/locale/3477/days/15?token={os.getenv("tokenAdvisor")}'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
        if resp.status_code != 200:
            raise Exception("")
        
        return resp.json()

