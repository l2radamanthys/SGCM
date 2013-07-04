

import sqlite3
import psycopg2
import os, sys
from random import choice

from django.contrib.auth.models import User
#from django.contrib.auth.models import Group as DjangoGroup
#from GestionTurnos.models import UserInformation

proyect_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(proyect_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#constant
ABC = "0123456789abcdefghijklmnopqrstuvwxyz"
DB_PATH = "../media/export/sgcm_alt.db"
QUERY = "SELECT * FROM auth_user as user JOIN UsersInformation as info ON user.id = info.user_id JOIN auth_user_groups as grop ON user.id = grop.user_id"


def is_exist(cur, tbl, field, field_v):
    cur.execute("SELECT COUNT(*) FROM %s WHERE %s='%s'" %(tbl, field, field_v))
    return cur.fetchone()[0]


def get_id(cur, username):
    cur.execute("SELECT id FROM auth_user WHERE username='%s'" %(username))
    return cur.fetchone()[0]


def main():
    #sqlite connection
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    a_cur = conn.cursor() #alternative cursor

    #posgre connection
    conn = psycopg2.connect("dbname='SGCM_DB' user='wyrven' host='localhost' password='inmortal'")
    pcur = conn.cursor()

    cur.execute(QUERY)
    for row in cur:
        if row[1] == u'admin':
            continue

        if is_exist(pcur, 'auth_user', 'username', row[1]):
            user = row[1] + choice(ABC) + choice(ABC)
        else:
            user = row[1]
        print row

        #_user = User.objects.create_user(
            #username=user,
            #email=row[4],
            #password="123456"
        #)







if __name__ == '__main__':
    main()
