import os, httpx, logging, uuid

from datetime import datetime, timedelta
from application.models.InformationDayForecast import InformationDayForecast

from application.service.WeatherForecastBase import WeatherForecastBase

class ForecastHGBrasil(WeatherForecastBase):

    def __init__(self) -> None:
        self.source = 'HGBrasil'
        self.city = 'SAO PAULO'

    async def get_prediction_minus_x(self, x_days):
        logging.info(f"Get predictions - {self.source}")
        current_date = datetime.now()
        data_mais_x = current_date + timedelta(days=x_days)
        data_key = data_mais_x.strftime('%d/%m')

        for dia_info in self.json_forecast['results']['forecast']:
            if dia_info['date'] == data_key:
                cd_dia = int(data_mais_x.strftime('%Y-%m-%d').replace('-', '')) 
                dici = {
                        "id": str(uuid.uuid4()),
                        'cd_dia': cd_dia,
                        'x_dias': x_days,
                        f'dia_previsao_feita_menos_x': str(current_date.date()),
                        'fonte': self.source,
                        'cidade': self.city,
                        'descricao': dia_info['description']
                    }
                if x_days == 0:
                    dici.update({
                        f'temperatura_real_min': dia_info['min'],
                        f'temperatura_real_max':  dia_info['max'], 
                    })
                else: 
                    dici.update({
                        f'temperatura_min_previsao_feita_menos_x': dia_info['min'],
                        f'temperatura_max_previsao_feita_menos_x':  dia_info['max'],
                    })
                return InformationDayForecast(**dici)
        
        return None

    async def request_forecast(self):
        url = os.getenv("urlHGBrasil")
        url = f'{url}?woeid=455827%20'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
        logging.info(f"Response - Request - {self.source}: {resp.status_code}")
        if resp.status_code != 200:
            raise Exception(f"Error - Request - {self.source}", resp.text)
        
        return resp.json()