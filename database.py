import pymysql
from app import app

def get_connection():
    return pymysql.connect(host=app.config['db.luddy.indiana.edu'],
                           user=app.config['jtcho'],
                           password=app.config['jt0405@(^*ssh3082WP'],
                           database=app.config['i211f22_jtcho'],
                           cursorclass=pymysql.cursors.DictCursor)

def get_courses():
    sql = "select * from courses order by start_date"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

def get_course(course_id):
    sql = "select * from courses where id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (course_id))
            return cursor.fetchone()

def add_course(name, pet, level, start_date, start_time, duration, length, trainer_name, description):
    sql = "insert into courses (name, pet, level, start_date, start_time, duration, length, trainer_name, description) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, pet, level, start_date, start_time, duration, length, trainer_name, description))
        conn.commit()

def update_course(course_id, name, pet, level, start_date, start_time, duration, length, trainer_name, description):
    sql = "update courses set name=%s, pet=%s, level=%s, start_date=%s, start_time=%s, duration=%s, length=%s, trainer_name=%s, description=%s where id='%s'"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, pet, level, start_date, start_time, duration, length, trainer_name, description, course_id))
        conn.commit()

def get_attendees():
    sql = "select * from attendees order by id"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

def add_attendee(course_id, first_name, last_name, phone_number, email, birth_date):
    sql = "insert into attendees (first_name, last_name, phone_number, email, birth_date, course_id) values (%s, %s, %s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (first_name, last_name, phone_number, email, birth_date, course_id))
        conn.commit()

def edit_attendee(attendee_id, course_id, first_name, last_name, phone_number, email, birth_date):
    sql = "update attendees set first_name=%s, last_name=%s, phone_number=%s, email=%s, birth_date=%s, course_id=%s where id='%s'"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (first_name, last_name, phone_number, email, birth_date, course_id, attendee_id))
        conn.commit()

def delete_attendee(attendee_id):
    sql = "delete from attendees where id='%s'"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (attendee_id))
        conn.commit()
                           