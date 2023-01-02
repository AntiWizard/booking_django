def insert_airport(conn, ids, flag=True):
    ids = [id[0] for id in ids]
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = [['mehr_adad'],
                ['shiraz'],
                ['esfahan'],
                ['berlin'],
                ['milan']]
        for i in range(len(ids)):
            data[i].append(ids[i])
        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO airplane_airport(title, address_id)"
                "VALUES (%s, %s)", d)

        print("ADD airport")


def insert_airport_terminal(conn, ids, flag=True):
    ids = [id[0] for id in ids]
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = []
        for id in ids:
            for j in range(1, 6):
                data.append([j, id])

        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO airplane_airportterminal(number, is_valid, created_time, modified_time, airport_id)"
                "VALUES (%s,TRUE,now(),now(), %s)", d)

        print("ADD airport terminal")


def insert_airplane_company(conn, ids, flag=True):
    ids = [id[0] for id in ids]
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = []
        for id in ids:
            data.append(["company-" + str(id), id])

        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO airplane_airplanecompany(name, is_valid, created_time, modified_time, airport_terminal_id)"
                "VALUES (%s,TRUE,now(),now(), %s)", d)

        print("ADD airport terminal company")


def insert_airplane(conn, ids, flag=True):
    ids = [id[0] for id in ids]
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data, i = [], 0
        for id in ids:
            data.append([100 + i, "", 100, 0, 'SPACE', 'pilot-' + str(id), id, 2, 1])
            i += 1

        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO airplane_airplane(transport_number, description, max_reservation,"
                " number_reserved, transfer_date, duration, transport_status, is_valid,"
                " created_time, modified_time, pilot, company_id, destination_id, source_id)"
                "VALUES (%s,%s,%s,%s,TIMESTAMP '2023-01-01 12:00:00',TIME '01:30:00',%s,TRUE,now(),now(), %s,%s,%s,%s)",
                d)

        print("ADD airplane")


def insert_seat(conn, airplane_ids, price_ids, flag=True):
    ids = [id[0] for id in price_ids]
    info = [list(d) for d in airplane_ids]  # 0->id ,1->max_reservation
    if flag and conn.status == 1:
        cursor = conn.cursor()
        data = []
        for i in range(len(info)):
            for number in range(1, info[i][1] + 1):
                data.append([number, 'FREE', info[i][0], ids[int(i / (int(len(info) / len(ids))))]])

        data = [tuple(item) for item in data]

        for d in data:
            cursor.execute(
                "INSERT INTO airplane_airplaneseat(number, status, is_valid, created_time,"
                " modified_time, airplane_id, price_id)"
                "VALUES (%s,%s,True,now(),now(), %s,%s)", d)

        print("ADD airplane seat")
