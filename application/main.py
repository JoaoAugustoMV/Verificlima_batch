
import asyncio

from application.service.WeatherForecastBase import WeatherForecastBase
from application.service.ForecastAdvisor import ClimaAdvisorService 
from application.service.ForecastHGBrasil import ForecastHGBrasil


listaServices: list[WeatherForecastBase] = [ClimaAdvisorService(),   ForecastHGBrasil()]
async def main():
    await asyncio.gather(
        *[service.save_temperatures_predictions() for service in listaServices]
    )
