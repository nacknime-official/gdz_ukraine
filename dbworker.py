import psycopg2
from config import dbname, user, password, host
import ipdb

connection = psycopg2.connect(dbname=dbname, user=user,
                              password=password,
                              host=host)
cursor = connection.cursor()

# state
def get_current_state(user_id):
    with connection:
        try:
            cursor.execute("""
                SELECT state
                FROM users
                WHERE user_id = (%s)
                """, (str(user_id),))
            return cursor.fetchone()[0]
        except:
            pass

def set_state(state, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET state = (%s)
            WHERE user_id = (%s)
            """, (state, str(user_id)))
        connection.commit()

# user_id
def get_and_set_id(user_id):
    with connection:
        cursor.execute(
            "SELECT 1 FROM users WHERE user_id = (%s)", (str(user_id),))
        a = cursor.fetchone()
        if a is None:
            cursor.execute("""
                        INSERT INTO users (user_id, klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise, state) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (str(user_id), 1, 'None', 'None', 'None', 'None', 'None', 'None', 'None', 0))
            connection.commit()

# klas
def get_klas(user_id):
    with connection:
        cursor.execute("""
            SELECT klas
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_klas(klas, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET klas = (%s)
            WHERE user_id = (%s)
            """, (klas, str(user_id)))
        connection.commit()

# subject
def get_subjects(klas):
    with connection:
        cursor.execute("""
            SELECT distinct subject from gdz
            WHERE klas = (%s)
            ORDER BY subject
            """, (klas,))
        return cursor.fetchall()

def set_subject(subject, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET subject = (%s)
            WHERE user_id = (%s)
            """, (subject, str(user_id)))
        connection.commit()

def get_subject(user_id):
    with connection:
        cursor.execute("""
            SELECT subject
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

# author
def get_authors(klas, subject):
    with connection:
        cursor.execute("""
                SELECT distinct author from gdz
                WHERE klas = (%s) AND subject = (%s)
                ORDER BY author
                """, (klas, subject))
        return cursor.fetchall()

def get_author(user_id):
    with connection:
        cursor.execute("""
            SELECT author
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_author(author, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET author = (%s)
            WHERE user_id = (%s)
            """, (author, str(user_id)))
        connection.commit()

# types
def get_types(klas, subject, author):
    with connection:
        cursor.execute("""
                SELECT distinct type from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s)
                ORDER BY type
                """, (klas, subject, author))
        return cursor.fetchall()

def get_type(user_id):
    with connection:
        cursor.execute("""
            SELECT type
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_type(type, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET type = (%s)
            WHERE user_id = (%s)
            """, (type, str(user_id)))
        connection.commit()

# maintopic
def get_maintopics(klas, subject, author, type):
    with connection:
        cursor.execute("""
                SELECT distinct maintopic from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s)
                ORDER BY maintopic
                """, (klas, subject, author, type))
        return cursor.fetchall()

def get_maintopic(user_id):
    with connection:
        cursor.execute("""
            SELECT maintopic
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_maintopic(maintopic, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET maintopic = (%s)
            WHERE user_id = (%s)
            """, (maintopic, str(user_id)))
        connection.commit()

# subtopic
def get_subtopics(klas, subject, author, type, maintopic):
    with connection:
        cursor.execute("""
                SELECT distinct subtopic from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s)
                ORDER BY subtopic
                """, (klas, subject, author, type, maintopic))
        return cursor.fetchall()

def get_subtopic(user_id):
    with connection:
        cursor.execute("""
            SELECT subtopic
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_subtopic(subtopic, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET subtopic = (%s)
            WHERE user_id = (%s)
            """, (subtopic, str(user_id)))
        connection.commit()

# subsubtopic
def get_subsubtopics(klas, subject, author, type, maintopic, subtopic):
    with connection:
        cursor.execute("""
                SELECT distinct subsubtopic from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s)
                ORDER BY subsubtopic
                """, (klas, subject, author, type, maintopic, subtopic))
        return cursor.fetchall()

def get_subsubtopic(user_id):
    with connection:
        cursor.execute("""
            SELECT subsubtopic
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_subsubtopic(subsubtopic, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET subsubtopic = (%s)
            WHERE user_id = (%s)
            """, (subsubtopic, str(user_id)))
        connection.commit()

# exercise
def get_exercises(klas, subject, author, type, maintopic, subtopic, subsubtopic):
    with connection:
        # ipdb.set_trace()
        cursor.execute("""
                SELECT exercise
                FROM gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s) AND subsubtopic = (%s)
                ORDER BY case when try_cast_int(exercise) is not null then exercise::int else 0 end
                """, (klas, subject, author, type, maintopic, subtopic, subsubtopic))
        return cursor.fetchall()

def get_exercise(user_id):
    with connection:
        cursor.execute("""
            SELECT exercise
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]

def set_exercise(exercise, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET exercise = (%s)
            WHERE user_id = (%s)
            """, (exercise, str(user_id)))
        connection.commit()

# solution
def get_solution(klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise):
    with connection:
        cursor.execute("""
            SELECT solution_id
            FROM gdz
            WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s) AND subsubtopic = (%s) AND exercise = (%s)
            """, (klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise))
        sol_id = cursor.fetchone()[0]
        if not sol_id:
            cursor.execute("""
                SELECT exercise_url
                FROM gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s) AND subsubtopic = (%s) AND exercise = (%s)
                """, (klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise))
            return cursor.fetchone()[0]
        else:
            return sol_id

def set_solution(klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise, solution_id):
    with connection:
        cursor.execute("""
            UPDATE gdz
            SET solution_id = (%s)
            WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s) AND subsubtopic = (%s) AND exercise = (%s)
            """, (solution_id, klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise))
        connection.commit()

# save keyboards for 'back' func
def set_keyboard_and_msg(data, user_id):
    with connection:
        cursor.execute("""
            UPDATE users
            SET markup = (%s)
            WHERE user_id = (%s)
            """, (psycopg2.Binary(data), str(user_id)))
        connection.commit()

def get_keyboard_and_msg(user_id):
    # ipdb.set_trace()
    with connection:
        cursor.execute("""
            SELECT markup
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        return cursor.fetchone()[0]
