import psycopg2
from connect import conn
from datetime import date, datetime
from sent_email import send_email
try:
    # create a cursor
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


def main(data):
    print(f"Choose your room!".center(50, "-"))
    room_number  = input(" №1 Room,  №2 Room,  №3 Room,  №4 Room,  №5 Room:")
    
    if not room_number.isdigit() or not 0 < int(room_number) <= 5:
        print("Choose your room number!")
        main(data)

    def get_book_list(data): #to get bokk info list to get informed
        try:
            list_query = f""" select room_id, book_start, book_end from queue where room_id='{data["room_id"]}' """
            cur.execute(list_query)
            conn.commit()
            record = cur.fetchall()
            print(f" №{data['room_id']} Room, book list info!".center(50,"+"))
            if record:
                for index,i in enumerate(record):
                    print(index+1, ')', 'from', i[1].strftime("%d/%m/%Y"), 'to', i[2].strftime("%d/%m/%Y"))
            else:
                print("No booking data for this room yet!")
            print("-".center(50,"-"))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    get_book_list({"room_id":room_number})

    def is_empty(data): #to check if room is empty
        try:
            check_query = f"""select exists(select 1 from queue where 
            room_id='{data['room_id']}' and '{data['book_start']}' >= book_start and '{data['book_start']}' < book_end 
            or room_id='{data['room_id']}' and '{data['book_end']}' > book_start and '{data['book_end']}' <= book_end 
            or room_id='{data['room_id']}' and '{data['book_start']}' < book_start and '{data['book_end']}' > book_end); """
            cur.execute(check_query)
            conn.commit()
            record = cur.fetchone()
            return record[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return False

    def book(): #room booking  proccess
        print("To go back to choose rooms enter back.")

        book_start = input("Start time <Example day/month/YYYY> //:")
        if book_start == "back":
            main(data)
        book_end = input("End time <Example day/month/YYYY> //:")
        if book_end == "back":
            main(data)
 
        try:
            book_start = datetime.strptime(book_start,'%d/%m/%Y').date()
            book_end = datetime.strptime(book_end,'%d/%m/%Y').date()
        except Exception as ex:
            print(ex)
            book()
        #time validations
        if  type(book_start) != date or  type(book_end) != date: #Validate date
            print("---Please enter date as an <Example dd/mm/YYYY>!---")
            book()
        elif book_start < datetime.now().date() or book_end < datetime.now().date() or book_start > book_end or book_start == book_end:
            print("---Please enter valid real date!---")
            book()
        else:
            try:
                if is_empty({"room_id":int(room_number), "book_start":book_start, "book_end":book_end}):
                    print(f"№{room_number} Room booked in this period of time! Choose another date!")
                    main(data)
                
                insert_query = """ INSERT INTO queue (user_id, room_id, book_start, book_end) VALUES ('{}', '{}', '{}', '{}')""".format(data['user_id'], int(room_number), book_start, book_end)
                cur.execute(insert_query)
                conn.commit()
                cur.execute(f"SELECT * from queue where book_start='{book_start}'")
                record = cur.fetchone()
                if record != None:
                    send_or_not = input("Do you want to send info. about your book to your email? yes/no:")
                    if send_or_not == "yes":
                        print('Loading...')
                        send_email({"to_user":data['email'], 'subject':'Booked a room!', 'body':f"Your room is {room_number}, from {book_start} to {book_end}!"})

                    print(f"Your room is {room_number}, from {book_start} to {book_end}!")
                    print("Done".center(50,'-'))

                    back_or_end = input("Finish or back to rooms? room/end:")
                    if back_or_end == "room":
                        main(data)
                    else:
                        return
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                main(data)
    book()

    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()
        cur.close()
