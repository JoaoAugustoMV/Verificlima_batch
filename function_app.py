import os, sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging, traceback

import azure.functions as func
import asyncio
from application.main import main

app = func.FunctionApp()

@app.schedule(schedule="0 0 9 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=True) 
def batch_verificlima(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info(f'Starting batch - {datetime.now()}...')
    try:
        asyncio.run(main())
    except Exception as e: 
        logging.error(f"{traceback.format_exc()}")
        logging.error(e)
        
    logging.info(f'Finalizando a função - {datetime.now()}')