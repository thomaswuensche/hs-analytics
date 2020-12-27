import logging
import os
import psycopg2 as pg
from controller import AnalyticsController

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import util

util.set_logging_config()
api = util.spotipy_client()

db_conn = pg.connect(os.environ['DATABASE_URL'], sslmode='require')
logging.info(f'connected to db: {db_conn.dsn}')

result = api.playlist_tracks(os.environ['PLAYLIST_HS'])

controller = AnalyticsController(api, db_conn)
controller.reset_table(os.environ['DB_TABLE_HS'])
controller.process_result(result)

db_conn.close()
logging.info('db connection closed')
