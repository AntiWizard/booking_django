import psycopg2

from fake_data.address import insert_airport_address, insert_hotel_address
from fake_data.airplane import *
from fake_data.currency import insert_currency
from fake_data.hotel import insert_hotel, insert_room
from fake_data.price import insert_price


def hotel():
    insert_hotel_address(conn, False)
    cursor.execute("select id from hotel_hoteladdress")
    ids = cursor.fetchall()

    insert_hotel(conn, ids, False)
    cursor.execute("select id,room_count from hotel_hotel")
    info = cursor.fetchall()
    cursor.execute("select id from reservations_price")
    price_ids = cursor.fetchall()

    insert_room(conn, info, price_ids, False)


def airplane():
    insert_airport_address(conn, False)
    cursor.execute("select id from airplane_airportaddress")
    ids = cursor.fetchall()

    insert_airport(conn, ids, False)
    cursor.execute("select id from airplane_airport")
    airport_ids = cursor.fetchall()

    insert_airport_terminal(conn, airport_ids, False)
    cursor.execute("select id from airplane_airportterminal")
    airport_terminal_ids = cursor.fetchall()

    insert_airplane_company(conn, airport_terminal_ids, False)
    cursor.execute("select id from airplane_airplanecompany")
    airplane_company_ids = cursor.fetchall()

    insert_airplane(conn, airplane_company_ids, False)
    cursor.execute("select id,max_reservation from airplane_airplane")
    airplane_ids = cursor.fetchall()
    cursor.execute("select id from reservations_price")
    price_ids = cursor.fetchall()

    insert_seat(conn, airplane_ids, price_ids, False)


conn = psycopg2.connect(
    database="postgres", user='postgres', password='test', host='127.0.0.1', port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

insert_currency(conn, False)

cursor.execute("select id from reservations_currency")
ids = cursor.fetchall()
insert_price(conn, ids, False)

hotel()
airplane()

conn.commit()
conn.close()
