import psycopg2
from config import dbname, user, password, host


connection = psycopg2.connect(dbname=dbname, user=user,
                              password=password,
                              host=host)
cursor = connection.cursor()


# get all users
def get_all_users():
    with connection:
        cursor.execute("""
            SELECT user_id
            FROM users
            """)
        try:
            return [i[0] for i in cursor.fetchall()]
        except Exception as e:
            print(e)
            return None

# state
def get_current_state(user_id):
    with connection:
        cursor.execute("""
            SELECT state
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
            SELECT subject, max(id) from gdz
            WHERE klas = (%s)
            GROUP BY subject
            ORDER BY max(id)
            """, (klas,))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

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
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        return None

# author
def get_authors(klas, subject):
    with connection:
        cursor.execute("""
                SELECT author, max(id) from gdz
                WHERE klas = (%s) AND subject = (%s)
                GROUP BY author
                ORDER BY max(id)
                """, (klas, subject))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

def get_author(user_id):
    with connection:
        cursor.execute("""
            SELECT author
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
                SELECT type, max(id) from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s)
                GROUP BY type
                ORDER BY max(id)
                """, (klas, subject, author))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

def get_type(user_id):
    with connection:
        cursor.execute("""
            SELECT type
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
                SELECT maintopic, max(id) from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s)
                GROUP BY maintopic
                ORDER BY max(id)
                """, (klas, subject, author, type))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

def get_maintopic(user_id):
    with connection:
        cursor.execute("""
            SELECT maintopic
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
                SELECT subtopic, max(id) from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s)
                GROUP BY subtopic
                ORDER BY max(id)
                """, (klas, subject, author, type, maintopic))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

def get_subtopic(user_id):
    with connection:
        cursor.execute("""
            SELECT subtopic
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
                SELECT subsubtopic, max(id) from gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s)
                GROUP BY subsubtopic
                ORDER BY max(id)
                """, (klas, subject, author, type, maintopic, subtopic))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

def get_subsubtopic(user_id):
    with connection:
        cursor.execute("""
            SELECT subsubtopic
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
        cursor.execute("""
                SELECT exercise, max(id)
                FROM gdz
                WHERE klas = (%s) AND subject = (%s) AND author = (%s) AND type = (%s) AND maintopic = (%s) AND subtopic = (%s) AND subsubtopic = (%s)
                GROUP BY exercise
                ORDER BY max(id)
                """, (klas, subject, author, type, maintopic, subtopic, subsubtopic))
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None

def get_exercise(user_id):
    with connection:
        cursor.execute("""
            SELECT exercise
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None

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
            try:
                return cursor.fetchone()[0]
            except Exception as e:
                print(e)
                return None
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
    with connection:
        cursor.execute("""
            SELECT markup
            FROM users
            WHERE user_id = (%s)
            """, (str(user_id),))
        try:
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return None
