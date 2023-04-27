import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("work_data.db")
    except Error as e:
        print(e)
    return conn


def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS work_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE,
                        hours_worked FLOAT,
                        km_driven FLOAT
                      );""")
    conn.commit()


def insert_data(conn, date, hours_worked, km_driven):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO work_data (date, hours_worked, km_driven) VALUES (?, ?, ?)", (date, hours_worked, km_driven))
    conn.commit()


def update_data(conn, id, date, hours_worked, km_driven):
    cursor = conn.cursor()
    cursor.execute("UPDATE work_data SET date = ?, hours_worked = ?, km_driven = ? WHERE id = ?", (date, hours_worked, km_driven, id))
    conn.commit()


def delete_data(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM work_data WHERE id = ?", (id,))
    conn.commit()


def get_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work_data")
    return cursor.fetchall()


# ... (previous code)
import calendar

def default_hours_worked():
    today = datetime.today()
    weekday = today.weekday()  # Returns the day of the week as an integer (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)

    if weekday == 4:  # Friday
        return 7.0
    elif 0 <= weekday <= 3:  # Monday to Thursday
        return 7.5
    else:
        return 0.0


def main():
    st.title("Work Hours and Kilometers Tracker")
    st.write("A simple web app to track hours spent on work and kilometers driven.")

    conn = create_connection()
    init_db(conn)

    st.sidebar.header("Add new entry")
    date = st.sidebar.date_input("Date", value=datetime.today(), key="add_date")
    
    default_hours = default_hours_worked()
    hours_options = [round(x * 0.5, 1) for x in range(0, 49)]  # List of possible hours from 0 to 24 with 0.5 hour intervals
    hours_worked = st.sidebar.selectbox("Hours worked", options=hours_options, key="add_hours_worked", index=hours_options.index(default_hours))
    
    km_driven = st.sidebar.number_input("Kilometers driven", min_value=0.0, step=0.1, key="add_km_driven")

    if st.sidebar.button("Add entry"):
        insert_data(conn, date, hours_worked, km_driven)
        st.sidebar.success("Entry added successfully.")

    st.sidebar.header("Edit or delete entry")
    entry_id = st.sidebar.number_input("Entry ID", min_value=1, step=1, value=1)
    date_edit = st.sidebar.date_input("Date", value=datetime.today(), key="edit_date")
    
    hours_worked_edit = st.sidebar.selectbox("Hours worked", options=hours_options, key="edit_hours_worked", index=hours_options.index(default_hours))
    km_driven_edit = st.sidebar.number_input("Kilometers driven", min_value=0.0, step=0.1, key="edit_km_driven")

    if st.sidebar.button("Update entry"):
        update_data(conn, entry_id, date_edit, hours_worked_edit, km_driven_edit)
        st.sidebar.success("Entry updated successfully.")

    if st.sidebar.button("Delete entry"):
        delete_data(conn, entry_id)
        st.sidebar.success("Entry deleted successfully.")

    st.header("Work Data")
    data = get_all_data(conn)

    # Create a pandas DataFrame and display it using st.write
    df = pd.DataFrame(data, columns=["ID", "Date", "Hours Worked", "Kilometers Driven"])
    st.write(df)

if __name__ == "__main__":
    main()