def insert_currency(conn, flag=True):
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = [('dolar', 'USD'),
                ('rial', 'IRR'),
                ('euro', 'EUR')]

        for d in data:
            cursor.execute(
                "INSERT INTO reservations_currency(name, code)VALUES (%s, %s)", d)

        print("ADD currency")
