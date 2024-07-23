import os, httpx
from application.models.InformationDayForecast import InformationDayForecast


class APIService():
    urlBase = os.getenv("urlVerifiClimaBackend")

    async def insert_infos(self, infos: list[InformationDayForecast]) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f'{self.urlBase}/info_dia_temp', json=infos, timeout=60)

        return resp