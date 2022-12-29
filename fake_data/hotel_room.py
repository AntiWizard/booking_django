def insert_room(conn, info, price_ids, flag=True):
    ids = [id[0] for id in price_ids]
    info = [list(d) for d in info]  # 0->id ,1->room_count
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = []
        for i in range(len(info)):
            for number in range(1, info[i][1] + 1):
                data.append([number, '2', '', 'FREE', info[i][0], ids[i]])

        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO hotel_hotelroom(number, capacity, description, status, is_valid, created_time, modified_time, hotel_id, price_per_night_id)"
                "VALUES (%s,%s,%s,%s,True,now(),now(), %s,%s)", d)

        print("ADD hotel room")
