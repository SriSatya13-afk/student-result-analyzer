import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("students.db")
    df = pd.read_csv("students_clean.csv")
    df_db = df[["gender", "math", "reading", "writing", "average", "pass_fail"]]
    df_db.to_sql("students", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print("Database created successfully! ✅")

def get_top_students():
    conn = sqlite3.connect("students.db")
    df = pd.read_sql_query("""
        SELECT gender, math, reading, writing, ROUND(average, 1) as average
        FROM students
        ORDER BY average DESC
        LIMIT 5
    """, conn)
    conn.close()
    return df

def get_pass_fail_count():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pass_fail, COUNT(*) FROM students GROUP BY pass_fail")
    result = cursor.fetchall()
    conn.close()
    return result

def get_gender_stats():
    conn = sqlite3.connect("students.db")
    df = pd.read_sql_query("""
        SELECT gender,
               ROUND(AVG(math), 1) as avg_math,
               ROUND(AVG(reading), 1) as avg_reading,
               ROUND(AVG(writing), 1) as avg_writing
        FROM students
        GROUP BY gender
    """, conn)
    conn.close()
    return df

def get_subject_difficulty():
    conn = sqlite3.connect("students.db")

    df = pd.read_sql_query("SELECT math, reading, writing FROM students", conn)

    result = {}
    for subject in ["math", "reading", "writing"]:
        failures = int((df[subject] < 40).sum())
        avg = round(float(df[subject].mean()), 1)
        below60 = int((df[subject] < 60).sum())

        dist = {
            "0-40":   int((df[subject] <= 40).sum()),
            "41-60":  int(((df[subject] > 40) & (df[subject] <= 60)).sum()),
            "61-75":  int(((df[subject] > 60) & (df[subject] <= 75)).sum()),
            "76-90":  int(((df[subject] > 75) & (df[subject] <= 90)).sum()),
            "91-100": int((df[subject] > 90).sum()),
        }

        result[subject] = {
            "failures": failures,
            "avg": avg,
            "below60": below60,
            "dist": dist
        }

    subjects = sorted(result.items(), key=lambda x: x[1]["failures"], reverse=True)
    difficulty_labels = ["Hardest", "Medium", "Easiest"]
    for i, (subject, data) in enumerate(subjects):
        data["difficulty"] = difficulty_labels[i]
        data["rank"] = i + 1

    conn.close()
    return result

def get_overall_stats():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            ROUND(AVG(average), 1) as avg_score,
            ROUND(AVG(math), 1) as avg_math,
            ROUND(AVG(reading), 1) as avg_reading,
            ROUND(AVG(writing), 1) as avg_writing
        FROM students
    """)
    row = cursor.fetchone()
    conn.close()
    return {
        "total": row[0],
        "avg_score": row[1],
        "avg_math": row[2],
        "avg_reading": row[3],
        "avg_writing": row[4]
    }

if __name__ == "__main__":
    create_database()
    print("\nTop 5 Students:")
    print(get_top_students())
    print("\nPass/Fail Counts:")
    print(get_pass_fail_count())
    print("\nSubject Difficulty:")
    print(get_subject_difficulty())
    print("\nOverall Stats:")
    print(get_overall_stats())