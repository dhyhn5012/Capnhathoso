import pandas as pd
import plotly.express as px
from io import BytesIO

def create_excel_report(df: pd.DataFrame):
    """Chuyển đổi DataFrame thành file Excel trong bộ nhớ."""
    output = BytesIO() # Tạo một đối tượng BytesIO để lưu dữ liệu Excel tạm thời
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Ghi DataFrame vào sheet 'BaoCaoNhanSu', không bao gồm index
        df.to_excel(writer, index=False, sheet_name='BaoCaoNhanSu')
    processed_data = output.getvalue() # Lấy giá trị byte của file Excel
    return processed_data

def plot_status_pie(df: pd.DataFrame):
    """Vẽ biểu đồ tròn thể hiện tỷ lệ trạng thái cập nhật hồ sơ."""
    if df.empty or 'trang_thai' not in df.columns:
        return None # Trả về None nếu DataFrame rỗng hoặc không có cột 'trang_thai'
    status_counts = df['trang_thai'].value_counts().reset_index()
    status_counts.columns = ['Trạng thái', 'Số lượng'] # Đổi tên cột cho dễ đọc
    fig = px.pie(status_counts, names='Trạng thái', values='Số lượng',
                 title='Tỷ lệ Trạng thái Cập nhật Hồ sơ', hole=.3) # hole=.3 tạo biểu đồ donut
    fig.update_traces(textposition='inside', textinfo='percent+label') # Hiển thị phần trăm và nhãn bên trong
    return fig

def plot_department_bar(df: pd.DataFrame):
    """Vẽ biểu đồ cột thể hiện số lượng nhân viên theo khoa/phòng."""
    if df.empty or 'khoa_phong' not in df.columns:
        return None
    dept_counts = df['khoa_phong'].value_counts().reset_index()
    dept_counts.columns = ['Khoa/Phòng', 'Số lượng']
    fig = px.bar(dept_counts, x='Khoa/Phòng', y='Số lượng',
                 title='Thống kê theo Khoa/Phòng/Trung tâm', text_auto=True) # text_auto hiển thị giá trị trên cột
    return fig

def plot_title_bar(df: pd.DataFrame):
    """Vẽ biểu đồ cột thể hiện số lượng nhân viên theo chức danh."""
    if df.empty or 'chuc_danh' not in df.columns:
        return None
    title_counts = df['chuc_danh'].value_counts().reset_index()
    title_counts.columns = ['Chức danh', 'Số lượng']
    fig = px.bar(title_counts, x='Chức danh', y='Số lượng',
                 title='Thống kê theo Chức danh', text_auto=True)
    return fig

def plot_age_histogram(df: pd.DataFrame):
    """Vẽ biểu đồ histogram phân bổ độ tuổi."""
    if df.empty or 'tuoi' not in df.columns:
        return None
    fig = px.histogram(df, x='tuoi', nbins=10, # Chia thành 10 bins (khoảng) độ tuổi
                       title='Phân bổ Độ tuổi Nhân viên')
    return fig
