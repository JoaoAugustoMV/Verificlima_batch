import logging
from abc import ABC, abstractmethod
from datetime import datetime
        
from application.models.InformationDayForecast import InformationDayForecast
from application.service.APIService import APIService
from application.utils.configs import DAYS_TO_FORECAST


apiService = APIService()
class WeatherForecastBase(ABC):
            
    async def save_temperatures_predictions(self) -> None:
        logging.info("Advisor - save_temperatures_predictions")

        infos = [await self.get_prediction_minus_x(day) for day in DAYS_TO_FORECAST]            
        await self.__saveInfos([i.model_dump() for i in infos if i is not None])        

    @abstractmethod
    async def get_prediction_minus_x(self, x_days: int):
        pass

    @abstractmethod
    def request_forecast(self):
        pass
            
    async def __saveInfos(self, infos: list[InformationDayForecast]):
        logging.info(f'_saveInfos - {self.source} - {self.city}')

        return await apiService.insert_infos(infos)
        
