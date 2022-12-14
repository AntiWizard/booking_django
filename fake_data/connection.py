import psycopg2
from decouple import config

from address import insert_airport_address, insert_hotel_address
from airplane import *
from currency import insert_currency
from hotel import insert_hotel, insert_room
from price import insert_price


def hotel():
    insert_hotel_address(conn, True)
    cursor.execute("select id from hotel_hoteladdress")
    ids = cursor.fetchall()

    insert_hotel(conn, ids, True)
    cursor.execute("select id,room_count from hotel_hotel")
    info = cursor.fetchall()
    cursor.execute("select id from reservations_price")
    price_ids = cursor.fetchall()

    insert_room(conn, info, price_ids, True)


def airplane():
    insert_airport_address(conn, True)
    cursor.execute("select id from airplane_airportaddress")
    ids = cursor.fetchall()

    insert_airport(conn, ids, True)
    cursor.execute("select id from airplane_airport")
    airport_ids = cursor.fetchall()

    insert_airport_terminal(conn, airport_ids, True)
    cursor.execute("select id from airplane_airportterminal")
    airport_terminal_ids = cursor.fetchall()

    insert_airplane_company(conn, airport_terminal_ids, True)
    cursor.execute("select id from airplane_airplanecompany")
    airplane_company_ids = cursor.fetchall()

    insert_airplane(conn, airplane_company_ids, True)
    cursor.execute("select id,max_reservation from airplane_airplane")
    airplane_ids = cursor.fetchall()
    cursor.execute("select id from reservations_price")
    price_ids = cursor.fetchall()

    insert_seat(conn, airplane_ids, price_ids, True)


conn = psycopg2.connect(
    database=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASS'),
    host=config('DB_HOST'),
    port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

insert_currency(conn, True)

cursor.execute("select id from reservations_currency")
ids = cursor.fetchall()
insert_price(conn, ids, True)

hotel()
airplane()

conn.commit()
conn.close()
