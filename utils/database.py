import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Tên file cơ sở dữ liệu SQLite
DB_NAME = "employee_data.db"

# Sử dụng cache_resource để kết nối CSDL chỉ một lần và duy trì kết nối
@st.cache_resource
def get_db_connection():
    """Tạo và trả về một kết nối tới CSDL SQLite."""
    # check_same_thread=False là cần thiết cho Streamlit vì các luồng khác nhau có thể truy cập DB
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

def init_db():
    """Khởi tạo các bảng trong CSDL nếu chúng chưa tồn tại."""
    conn = get_db_connection()
    c = conn.cursor()
    # Bảng lưu thông tin nhân viên
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ho_ten TEXT NOT NULL,
            tuoi INTEGER NOT NULL,
            khoa_phong TEXT NOT NULL,
            chuc_danh TEXT NOT NULL,
            trang_thai TEXT NOT NULL,
            thoi_gian_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Bảng lưu các yêu cầu hỗ trợ
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            noi_dung TEXT NOT NULL,
            thoi_gian_gui TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit() # Lưu các thay đổi vào CSDL

def save_employee_data(ho_ten, tuoi, khoa_phong, chuc_danh, trang_thai):
    """Lưu thông tin nhân viên vào CSDL."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO employees (ho_ten, tuoi, khoa_phong, chuc_danh, trang_thai)
            VALUES (?, ?, ?, ?, ?)
        ''', (ho_ten, tuoi, khoa_phong, chuc_danh, trang_thai))
        conn.commit() # Xác nhận giao dịch
        return True
    except sqlite3.Error as e:
        st.error(f"Lỗi CSDL khi lưu thông tin nhân viên: {e}")
        return False

def save_support_request(noi_dung):
    """Lưu yêu cầu hỗ trợ vào CSDL."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO requests (noi_dung) VALUES (?)', (noi_dung,))
        conn.commit() # Xác nhận giao dịch
        return True
    except sqlite3.Error as e:
        st.error(f"Lỗi CSDL khi lưu yêu cầu hỗ trợ: {e}")
        return False

@st.cache_data(ttl=600)  # Cache dữ liệu trong 10 phút để tăng hiệu suất
def get_all_data():
    """Lấy toàn bộ dữ liệu nhân viên từ CSDL và trả về dưới dạng DataFrame."""
    conn = get_db_connection()
    try:
        # Đọc tất cả dữ liệu từ bảng 'employees' vào DataFrame
        df = pd.read_sql_query("SELECT ho_ten, tuoi, khoa_phong, chuc_danh, trang_thai, thoi_gian_cap_nhat FROM employees", conn)
        return df
    except Exception as e:
        st.error(f"Không thể tải dữ liệu từ CSDL: {e}")
        return pd.DataFrame() # Trả về DataFrame rỗng nếu có lỗi
