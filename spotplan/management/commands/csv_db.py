from django.core.management.base import BaseCommand, CommandError
import sqlite3
import pandas as pd
import pandas.io.sql as psql
 


class Command(BaseCommand):
  help = 'Closes the specified poll for voting'
  # def add_arguments(self, parser):
  #    parser.add_argument('poll_ids', nargs='+', type=int)
  def handle(self, *args, **options):
    df = pd.read_csv('test.csv')
    # sqlite3に接続
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.execute('CREATE TABLE articles  (place_adress,  place_name, headline , place_detail, place_adress,place_parking,place_access,place_opening,thumbnail,place_url)')
    df.to_sql('articles', con, if_exists='append', index=None)
    print('ok')
