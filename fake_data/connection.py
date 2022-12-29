import psycopg2

from fake_data.currency import insert_currency
from fake_data.hotel import insert_hotel
from fake_data.hotel_address import insert_address
from fake_data.hotel_room import insert_room
from fake_data.price import insert_price

conn = psycopg2.connect(
    database="postgres", user='postgres', password='test', host='127.0.0.1', port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

insert_currency(conn, False)

cursor.execute("select id from reservations_currency")
ids = cursor.fetchall()
insert_price(conn, ids, False)

insert_address(conn, False)
cursor.execute("select id from hotel_hoteladdress")
ids = cursor.fetchall()

insert_hotel(conn, ids, False)
cursor.execute("select id,room_count from hotel_hotel")
info = cursor.fetchall()
cursor.execute("select id from reservations_price")
price_ids = cursor.fetchall()

insert_room(conn, info, price_ids, True)

conn.commit()
conn.close()
