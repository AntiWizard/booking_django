def insert_price(conn, ids, flag=True):
    ids = [id[0] for id in ids]
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = [['10000000', '0'],
                ['5000000', '0'],
                ['7500000', '0'],
                ['100000000', '0'],
                ['50000000', '0']]
        for i in range(len(data)):
            data[i].append(ids[1])
        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO reservations_price(value, ratio, currency_id)"
                "VALUES (%s,%s,%s)", d)

        print("ADD price")
