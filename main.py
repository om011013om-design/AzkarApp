import flet as ft
import sqlite3
import os
import traceback
from datetime import datetime

# ==================== كاشف الأخطاء ====================
def main(page: ft.Page):
    try:
        # تشغيل التطبيق الطبيعي
        real_main(page)
    except Exception as e:
        # لو حصل خطأ، اعرضه على الشاشة بدل الشاشة البيضاء
        page.bgcolor = "white"
        page.scroll = "adaptive"
        page.add(
            ft.Column([
                ft.Icon("error_outline", color="red", size=50),
                ft.Text("حدث خطأ أثناء التشغيل:", color="red", size=20, weight="bold"),
                ft.Text(f"{e}", color="black", size=16),
                ft.Container(height=20),
                ft.Text("تفاصيل الخطأ للمبرمج:", color="grey", size=14),
                ft.Text(traceback.format_exc(), color="red", size=12, font_family="monospace")
            ])
        )
        page.update()

# ==================== كودك الأصلي (داخل دالة جديدة) ====================

def get_db_path():
    return "hisn_almuslim.db"

def init_database():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, icon TEXT, color TEXT, order_num INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS adhkar (id INTEGER PRIMARY KEY AUTOINCREMENT, category_id INTEGER, text TEXT, count INTEGER, current_count INTEGER DEFAULT 0, benefit TEXT, hadith TEXT, FOREIGN KEY (category_id) REFERENCES categories (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasbih (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, count INTEGER DEFAULT 0, target INTEGER DEFAULT 33, last_updated TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        insert_default_data(cursor)
        
    conn.commit()
    conn.close()

def insert_default_data(cursor):
    # بيانات مخففة للتجربة السريعة
    categories = [
        ("أذكار الصباح", "wb_sunny", "#10b981", 1),
        ("أذكار المساء", "nights_stay", "#6366f1", 2),
        ("أذكار الصلاة", "mosque", "#f59e0b", 3),
        ("أذكار النوم", "bedtime", "#8b5cf6", 4)
    ]
    cursor.executemany("INSERT INTO categories (name, icon, color, order_num) VALUES (?, ?, ?, ?)", categories)

def get_setting(key):
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except:
        return None

def real_main(page: ft.Page):
    # إعدادات الصفحة
    page.title = "حصن المسلم"
    page.rtl = True
    page.padding = 0
    page.scroll = "adaptive"
    
    # تحميل الخط (مع حماية)
    try:
        page.fonts = {"MyFont": "myfont.otf"}
        page.theme = ft.Theme(font_family="MyFont")
    except:
        print("Font not found")

    # تهيئة قاعدة البيانات
    init_database()

    # الواجهة البسيطة للتجربة
    
    def create_card(title, icon_name, color_hex):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon_name, size=40, color="white"),
                ft.Text(title, size=18, color="white")
            ], alignment="center", horizontal_alignment="center"),
            bgcolor=color_hex,
            padding=20,
            border_radius=15,
            height=120,
            width=160
        )

    # عرض الفئات
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT name, icon, color FROM categories")
    cats = cursor.fetchall()
    conn.close()

    grid = ft.Row([create_card(c[0], c[1], c[2]) for c in cats], wrap=True, alignment="center")

    page.add(
        ft.AppBar(title=ft.Text("حصن المسلم"), bgcolor="#10b981", center_title=True),
        ft.Container(content=grid, padding=20)
    )

if __name__ == "__main__":
    ft.app(target=main)
