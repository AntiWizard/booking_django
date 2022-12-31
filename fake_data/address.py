def insert_hotel_address(conn, flag=True):
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = [('989210481410', 'iran', 'tehran', 'blah blah blah'),
                ('989210581410', 'iran', 'shiraz', 'blah blah blah'),
                ('989210281410', 'iran', 'esfahan', 'blah blah blah'),
                ('989210181410', 'german', 'berlin', 'blah blah blah'),
                ('989210981410', 'italy', 'milan', 'blah blah blah')]

        for d in data:
            cursor.execute("INSERT INTO hotel_hoteladdress(phone, country, city, address)VALUES (%s, %s,%s, %s)", d)

        print("ADD hotel address")


def insert_airport_address(conn, flag=True):
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = [('989210481411', 'iran', 'tehran', 'blah blah blah'),
                ('989210581411', 'iran', 'shiraz', 'blah blah blah'),
                ('989210281411', 'iran', 'esfahan', 'blah blah blah'),
                ('989210181411', 'german', 'berlin', 'blah blah blah'),
                ('989210981411', 'italy', 'milan', 'blah blah blah')]

        for d in data:
            cursor.execute("INSERT INTO airplane_airportaddress(phone, country, city, address)VALUES (%s, %s,%s, %s)",
                           d)

        print("ADD airport address")
