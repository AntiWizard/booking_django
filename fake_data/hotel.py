def insert_hotel(conn, ids, flag=True):
    ids = [id[0] for id in ids]
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = [['tehran', '', 'SPACE', '5', '100'],
                ['shiraz', '', 'SPACE', '4', '50'],
                ['esfahan', '', 'SPACE', '3', '50'],
                ['berlin', '', 'SPACE', '5', '200'],
                ['milan', '', 'SPACE', '5', '150']]
        for i in range(len(ids)):
            data[i].append(ids[i])
        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO hotel_hotel(name, description, residence_status,is_valid,created_time,modified_time, star, room_count, address_id)"
                "VALUES (%s,%s,%s,True,now(),now(), %s,%s, %s)", d)

        print("ADD hotel")
