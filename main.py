import flet as ft
import sqlite3
import os
import sys
from datetime import datetime

# ==================== إعدادات المسارات ====================

def get_app_path():
    """الحصول على مسار التطبيق الصحيح"""
    try:
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.dirname(os.path.abspath(__file__))
    except:
        return "."

def get_db_path():
    """الحصول على مسار قاعدة البيانات"""
    try:
        # على أندرويد، استخدم مسار البيانات
        if "ANDROID_ROOT" in os.environ:
            data_dir = os.environ.get("FLET_APP_STORAGE_DATA", "/data/data")
            return os.path.join(data_dir, "hisn_almuslim.db")
        else:
            return os.path.join(get_app_path(), "hisn_almuslim.db")
    except:
        return "hisn_almuslim.db"

def get_font_path():
    """الحصول على مسار الخط"""
    try:
        return os.path.join(get_app_path(), "myfont.otf")
    except:
        return "myfont.otf"

# ==================== قاعدة البيانات ====================

def init_database():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        
        # جدول الفئات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon TEXT NOT NULL,
                color TEXT NOT NULL,
                order_num INTEGER DEFAULT 0
            )
        ''')
        
        # جدول الأذكار
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adhkar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                current_count INTEGER DEFAULT 0,
                benefit TEXT,
                hadith TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # جدول التسبيح
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasbih (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                count INTEGER DEFAULT 0,
                target INTEGER DEFAULT 33,
                last_updated TEXT
            )
        ''')
        
        # جدول الإعدادات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # إدخال البيانات الافتراضية
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            insert_default_data(cursor)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False

def insert_default_data(cursor):
    """إدخال البيانات الافتراضية"""
    
    # الفئات
    categories = [
        ("أذكار الصباح", "wb_sunny", "#10b981", 1),
        ("أذكار المساء", "nights_stay", "#6366f1", 2),
        ("أذكار الصلاة", "home", "#f59e0b", 3),
        ("أذكار النوم", "bedtime", "#8b5cf6", 4),
        ("أذكار القرآن", "menu_book", "#ec4899", 5),
        ("أذكار السفر", "flight", "#06b6d4", 6),
        ("أذكار الطعام", "restaurant", "#84cc16", 7),
        ("أذكار متنوعة", "star", "#f97316", 8),
    ]
    
    cursor.executemany(
        "INSERT INTO categories (name, icon, color, order_num) VALUES (?, ?, ?, ?)",
        categories
    )
    
    # أذكار الصباح
    morning_adhkar = [
        (1, "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", 1, 0, "من أذكار الصباح المباركة", "رواه أبو داود"),
        (1, "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ", 1, 0, "التوكل على الله في بداية اليوم", "رواه الترمذي"),
        (1, "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَىٰ عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ", 1, 0, "سيد الاستغفار", "رواه البخاري"),
        (1, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", 100, 0, "أفضل الكلام بعد القرآن", "رواه مسلم"),
        (1, "لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", 10, 0, "كانت له عدل عشر رقاب", "متفق عليه"),
        (1, "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", 3, 0, "حماية من كل شر", "رواه مسلم"),
        (1, "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", 3, 0, "لم يضره شيء", "رواه أبو داود والترمذي"),
        (1, "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ", 3, 0, "سؤال العافية", "رواه ابن ماجه"),
    ]
    
    # أذكار المساء
    evening_adhkar = [
        (2, "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ", 1, 0, "من أذكار المساء", "رواه أبو داود"),
        (2, "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ", 1, 0, "التوكل على الله", "رواه الترمذي"),
        (2, "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", 3, 0, "حماية من الشر", "رواه مسلم"),
        (2, "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ", 1, 0, "الاستعاذة من الهم", "رواه البخاري"),
        (2, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", 100, 0, "حُطت خطاياه وإن كانت مثل زبد البحر", "متفق عليه"),
        (2, "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ", 100, 0, "الاستغفار", "متفق عليه"),
    ]
    
    # أذكار الصلاة
    prayer_adhkar = [
        (3, "أَسْتَغْفِرُ اللَّهَ، أَسْتَغْفِرُ اللَّهَ، أَسْتَغْفِرُ اللَّهَ", 3, 0, "بعد السلام من الصلاة", "رواه مسلم"),
        (3, "اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ، تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ", 1, 0, "بعد الصلاة", "رواه مسلم"),
        (3, "سُبْحَانَ اللَّهِ", 33, 0, "التسبيح بعد الصلاة", "رواه مسلم"),
        (3, "الْحَمْدُ لِلَّهِ", 33, 0, "التحميد بعد الصلاة", "رواه مسلم"),
        (3, "اللَّهُ أَكْبَرُ", 33, 0, "التكبير بعد الصلاة", "رواه مسلم"),
        (3, "لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", 1, 0, "تمام المائة", "رواه مسلم"),
    ]
    
    # أذكار النوم
    sleep_adhkar = [
        (4, "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", 1, 0, "عند النوم", "رواه البخاري"),
        (4, "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ", 1, 0, "عند النوم", "رواه أبو داود"),
        (4, "سُبْحَانَ اللَّهِ", 33, 0, "قبل النوم", "متفق عليه"),
        (4, "الْحَمْدُ لِلَّهِ", 33, 0, "قبل النوم", "متفق عليه"),
        (4, "اللَّهُ أَكْبَرُ", 34, 0, "قبل النوم", "متفق عليه"),
    ]
    
    # أذكار القرآن
    quran_adhkar = [
        (5, "أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ", 1, 0, "قبل القراءة", ""),
        (5, "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", 1, 0, "البسملة", ""),
        (5, "صَدَقَ اللَّهُ الْعَظِيمُ", 1, 0, "بعد الانتهاء من القراءة", ""),
    ]
    
    # أذكار السفر
    travel_adhkar = [
        (6, "اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَٰذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ", 1, 0, "دعاء السفر", "رواه مسلم"),
        (6, "اللَّهُمَّ إِنَّا نَسْأَلُكَ فِي سَفَرِنَا هَٰذَا الْبِرَّ وَالتَّقْوَىٰ", 1, 0, "دعاء السفر", "رواه مسلم"),
        (6, "اللَّهُمَّ هَوِّنْ عَلَيْنَا سَفَرَنَا هَٰذَا وَاطْوِ عَنَّا بُعْدَهُ", 1, 0, "تسهيل السفر", "رواه مسلم"),
    ]
    
    # أذكار الطعام
    food_adhkar = [
        (7, "بِسْمِ اللَّهِ", 1, 0, "قبل الأكل", "رواه أبو داود"),
        (7, "بِسْمِ اللَّهِ أَوَّلَهُ وَآخِرَهُ", 1, 0, "إذا نسي التسمية في أوله", "رواه أبو داود"),
        (7, "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَٰذَا، وَرَزَقَنِيهِ، مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ", 1, 0, "بعد الأكل", "رواه أبو داود"),
    ]
    
    # أذكار متنوعة
    misc_adhkar = [
        (8, "لَا إِلَٰهَ إِلَّا اللَّهُ", 100, 0, "أفضل الذكر", "رواه الترمذي"),
        (8, "سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَٰهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ", 100, 0, "الباقيات الصالحات", "رواه مسلم"),
        (8, "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", 100, 0, "كنز من كنوز الجنة", "متفق عليه"),
        (8, "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَىٰ نَبِيِّنَا مُحَمَّدٍ", 100, 0, "الصلاة على النبي", "رواه مسلم"),
    ]
    
    # إدخال جميع الأذكار
    all_adhkar = (morning_adhkar + evening_adhkar + prayer_adhkar + 
                  sleep_adhkar + quran_adhkar + travel_adhkar + 
                  food_adhkar + misc_adhkar)
    
    cursor.executemany(
        "INSERT INTO adhkar (category_id, text, count, current_count, benefit, hadith) VALUES (?, ?, ?, ?, ?, ?)",
        all_adhkar
    )
    
    # إدخال التسبيحات الافتراضية
    tasbihat = [
        ("سُبْحَانَ اللَّهِ", 0, 33, datetime.now().isoformat()),
        ("الْحَمْدُ لِلَّهِ", 0, 33, datetime.now().isoformat()),
        ("اللَّهُ أَكْبَرُ", 0, 34, datetime.now().isoformat()),
        ("لَا إِلَٰهَ إِلَّا اللَّهُ", 0, 100, datetime.now().isoformat()),
        ("أَسْتَغْفِرُ اللَّهَ", 0, 100, datetime.now().isoformat()),
    ]
    
    cursor.executemany(
        "INSERT INTO tasbih (name, count, target, last_updated) VALUES (?, ?, ?, ?)",
        tasbihat
    )
    
    # إعدادات افتراضية
    settings = [
        ("dark_mode", "false"),
        ("font_size", "18"),
    ]
    
    cursor.executemany(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        settings
    )

# ==================== وظائف قاعدة البيانات ====================

def get_categories():
    """الحصول على جميع الفئات"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY order_num")
        categories = cursor.fetchall()
        conn.close()
        return categories
    except:
        return []

def get_adhkar_by_category(category_id):
    """الحصول على الأذكار حسب الفئة"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adhkar WHERE category_id = ?", (category_id,))
        adhkar = cursor.fetchall()
        conn.close()
        return adhkar
    except:
        return []

def update_adhkar_count(adhkar_id, new_count):
    """تحديث عداد الذكر"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("UPDATE adhkar SET current_count = ? WHERE id = ?", (new_count, adhkar_id))
        conn.commit()
        conn.close()
    except:
        pass

def reset_adhkar_counts(category_id):
    """إعادة تعيين جميع العدادات لفئة معينة"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("UPDATE adhkar SET current_count = 0 WHERE category_id = ?", (category_id,))
        conn.commit()
        conn.close()
    except:
        pass

def get_tasbihat():
    """الحصول على جميع التسبيحات"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasbih")
        tasbihat = cursor.fetchall()
        conn.close()
        return tasbihat
    except:
        return []

def update_tasbih_count(tasbih_id, new_count):
    """تحديث عداد التسبيح"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasbih SET count = ?, last_updated = ? WHERE id = ?",
            (new_count, datetime.now().isoformat(), tasbih_id)
        )
        conn.commit()
        conn.close()
    except:
        pass

def reset_tasbih_count(tasbih_id):
    """إعادة تعيين عداد التسبيح"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasbih SET count = 0, last_updated = ? WHERE id = ?",
            (datetime.now().isoformat(), tasbih_id)
        )
        conn.commit()
        conn.close()
    except:
        pass

def get_setting(key, default=""):
    """الحصول على إعداد معين"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else default
    except:
        return default

def save_setting(key, value):
    """حفظ إعداد"""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
    except:
        pass

# ==================== التطبيق الرئيسي ====================

def main(page: ft.Page):
    """الدالة الرئيسية للتطبيق"""
    
    # الألوان الأساسية
    PRIMARY_COLOR = "#10b981"
    PRIMARY_DARK = "#059669"
    SECONDARY_COLOR = "#6366f1"
    
    # متغيرات الحالة
    state = {
        "dark_mode": False,
        "font_size": 18,
        "current_category_id": None,
        "current_tasbih_count": 0,
        "current_tasbih_target": 33,
    }
    
    def setup_page():
        """إعداد الصفحة الأساسية"""
        try:
            # تهيئة قاعدة البيانات
            init_database()
            
            # تحميل الإعدادات
            state["dark_mode"] = get_setting("dark_mode", "false") == "true"
            state["font_size"] = int(get_setting("font_size", "18"))
            
            # إعدادات الصفحة
            page.title = "حصن المسلم"
            page.rtl = True
            page.padding = 0
            page.spacing = 0
            page.scroll = ft.ScrollMode.AUTO
            page.theme_mode = ft.ThemeMode.DARK if state["dark_mode"] else ft.ThemeMode.LIGHT
            
            # محاولة تحميل الخط المخصص
            font_path = get_font_path()
            if os.path.exists(font_path):
                page.fonts = {"MyFont": font_path}
                page.theme = ft.Theme(font_family="MyFont")
                page.dark_theme = ft.Theme(font_family="MyFont")
            
            page.update()
        except Exception as e:
            print(f"Setup Error: {e}")
    
    def get_text_color():
        return "#FFFFFF" if state["dark_mode"] else "#1a1a1a"
    
    def get_bg_color():
        return "#1a1a2e" if state["dark_mode"] else "#f0f4f8"
    
    def get_card_color():
        return "#252542" if state["dark_mode"] else "#FFFFFF"
    
    def get_secondary_text_color():
        return "#a0a0a0" if state["dark_mode"] else "#666666"
    
    # ==================== المكونات ====================
    
    def create_header(title, show_back=False, show_settings=True):
        """إنشاء شريط العنوان"""
        
        back_btn = ft.Container(
            content=ft.IconButton(
                icon="arrow_forward",
                icon_color="#FFFFFF",
                icon_size=24,
                on_click=lambda e: show_home_page(),
            ),
            visible=show_back,
            width=48,
        )
        
        settings_btn = ft.Container(
            content=ft.IconButton(
                icon="settings",
                icon_color="#FFFFFF",
                icon_size=24,
                on_click=lambda e: show_settings_page(),
            ),
            visible=show_settings,
            width=48,
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    back_btn if show_back else ft.Container(width=48),
                    ft.Text(
                        title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                        text_align=ft.TextAlign.CENTER,
                        expand=True,
                    ),
                    settings_btn if show_settings else ft.Container(width=48),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=8, vertical=8),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[PRIMARY_COLOR, PRIMARY_DARK],
            ),
        )
    
    def create_category_card(category):
        """إنشاء بطاقة الفئة"""
        try:
            cat_id, name, icon, color, order = category
            
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                name=icon,
                                size=36,
                                color="#FFFFFF",
                            ),
                            width=64,
                            height=64,
                            border_radius=32,
                            bgcolor=color,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            name,
                            size=state["font_size"] - 2,
                            weight=ft.FontWeight.W_600,
                            color=get_text_color(),
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=16,
                border_radius=16,
                bgcolor=get_card_color(),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color="#1a000000",
                    offset=ft.Offset(0, 2),
                ),
                on_click=lambda e, cid=cat_id, cname=name: show_adhkar_page(cid, cname),
            )
        except Exception as e:
            print(f"Card Error: {e}")
            return ft.Container()
    
    def create_adhkar_card(dhikr, category_color):
        """إنشاء بطاقة الذكر"""
        try:
            dhikr_id, cat_id, text, count, current_count, benefit, hadith = dhikr
            remaining = max(0, count - current_count)
            is_completed = remaining <= 0
            
            counter_container = ft.Container(
                content=ft.Text(
                    "✓" if is_completed else str(remaining),
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF",
                ),
                width=56,
                height=56,
                border_radius=28,
                bgcolor="#22c55e" if is_completed else category_color,
                alignment=ft.alignment.center,
            )
            
            def on_tap(e):
                nonlocal remaining, is_completed, current_count
                if remaining > 0:
                    current_count += 1
                    remaining = max(0, count - current_count)
                    is_completed = remaining <= 0
                    update_adhkar_count(dhikr_id, current_count)
                    
                    if is_completed:
                        counter_container.bgcolor = "#22c55e"
                        counter_container.content = ft.Text(
                            "✓",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        )
                    else:
                        counter_container.content = ft.Text(
                            str(remaining),
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        )
                    page.update()
            
            counter_container.on_click = on_tap
            
            card_content = [
                # نص الذكر
                ft.Container(
                    content=ft.Text(
                        text,
                        size=state["font_size"],
                        weight=ft.FontWeight.W_500,
                        color=get_text_color(),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=16,
                ),
                
                ft.Divider(height=1, color="#e0e0e0" if not state["dark_mode"] else "#404040"),
                
                # زر العداد
                ft.Container(
                    content=ft.Row(
                        controls=[
                            counter_container,
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"العدد الكلي: {count}",
                                        size=state["font_size"] - 4,
                                        color=get_secondary_text_color(),
                                    ),
                                    ft.Text(
                                        "✓ اكتمل" if is_completed else f"متبقي: {remaining}",
                                        size=state["font_size"] - 4,
                                        color="#22c55e" if is_completed else category_color,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=16,
                    ),
                    padding=12,
                ),
            ]
            
            # إضافة الفائدة والحديث إذا وجدا
            if benefit or hadith:
                benefit_content = []
                if benefit:
                    benefit_content.append(
                        ft.Text(
                            benefit,
                            size=state["font_size"] - 4,
                            color=get_secondary_text_color(),
                            text_align=ft.TextAlign.CENTER,
                        )
                    )
                if hadith:
                    benefit_content.append(
                        ft.Text(
                            hadith,
                            size=state["font_size"] - 5,
                            color=get_secondary_text_color(),
                            italic=True,
                            text_align=ft.TextAlign.CENTER,
                        )
                    )
                
                card_content.append(
                    ft.Container(
                        content=ft.Column(
                            controls=benefit_content,
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(bottom=12, left=16, right=16),
                    )
                )
            
            return ft.Container(
                content=ft.Column(
                    controls=card_content,
                    spacing=0,
                ),
                margin=ft.margin.only(bottom=12, left=12, right=12),
                border_radius=12,
                bgcolor=get_card_color(),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=6,
                    color="#1a000000",
                    offset=ft.Offset(0, 2),
                ),
            )
        except Exception as e:
            print(f"Adhkar Card Error: {e}")
            return ft.Container()
    
    def create_tasbih_item(tasbih):
        """إنشاء عنصر التسبيح"""
        try:
            tasbih_id, name, count, target, last_updated = tasbih
            progress = min(count / target, 1.0) if target > 0 else 0
            
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                str(count),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=PRIMARY_COLOR,
                            ),
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor="#e6f7f1" if not state["dark_mode"] else "#1a3d32",
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    name,
                                    size=state["font_size"] - 2,
                                    weight=ft.FontWeight.W_600,
                                    color=get_text_color(),
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Container(
                                                width=120 * progress,
                                                height=4,
                                                bgcolor=PRIMARY_COLOR,
                                                border_radius=2,
                                            ),
                                            width=120,
                                            height=4,
                                            bgcolor="#e0e0e0" if not state["dark_mode"] else "#404040",
                                            border_radius=2,
                                        ),
                                        ft.Text(
                                            f"{count}/{target}",
                                            size=11,
                                            color=get_secondary_text_color(),
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=6,
                            expand=True,
                        ),
                        ft.Icon(
                            name="chevron_left",
                            color=get_secondary_text_color(),
                            size=20,
                        ),
                    ],
                    spacing=12,
                ),
                padding=14,
                margin=ft.margin.only(bottom=8, left=12, right=12),
                border_radius=10,
                bgcolor=get_card_color(),
                on_click=lambda e, tid=tasbih_id, tname=name, tc=count, tt=target: show_tasbih_page(tid, tname, tc, tt),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color="#1a000000",
                    offset=ft.Offset(0, 1),
                ),
            )
        except Exception as e:
            print(f"Tasbih Item Error: {e}")
            return ft.Container()
    
    # ==================== الصفحات ====================
    
    def show_home_page():
        """عرض الصفحة الرئيسية"""
        try:
            categories = get_categories()
            tasbihat = get_tasbihat()
            
            # بناء الواجهة
            content_list = [
                create_header("حصن المسلم", show_back=False, show_settings=True),
                
                # البطاقة الترحيبية
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "✨",
                                size=28,
                            ),
                            ft.Text(
                                "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                                size=state["font_size"] + 2,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "أذكار من الكتاب والسنة",
                                size=state["font_size"] - 3,
                                color="#e0e0e0",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=6,
                    ),
                    padding=20,
                    margin=12,
                    border_radius=12,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[PRIMARY_COLOR, SECONDARY_COLOR],
                    ),
                ),
                
                # عنوان الأقسام
                ft.Container(
                    content=ft.Text(
                        "📚 أقسام الأذكار",
                        size=state["font_size"],
                        weight=ft.FontWeight.BOLD,
                        color=get_text_color(),
                    ),
                    padding=ft.padding.only(right=16, top=8, bottom=8),
                ),
            ]
            
            # شبكة الفئات
            if categories:
                categories_grid = ft.GridView(
                    controls=[create_category_card(cat) for cat in categories],
                    runs_count=2,
                    max_extent=170,
                    child_aspect_ratio=1.0,
                    spacing=12,
                    run_spacing=12,
                    padding=12,
                )
                content_list.append(categories_grid)
            
            # عنوان التسبيح
            content_list.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("📿", size=20),
                            ft.Text(
                                "التسبيح الإلكتروني",
                                size=state["font_size"],
                                weight=ft.FontWeight.BOLD,
                                color=get_text_color(),
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.only(right=16, top=12, bottom=8),
                )
            )
            
            # قائمة التسبيحات
            if tasbihat:
                for t in tasbihat:
                    content_list.append(create_tasbih_item(t))
            
            content_list.append(ft.Container(height=20))
            
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        controls=content_list,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                    ),
                    bgcolor=get_bg_color(),
                    expand=True,
                )
            )
            page.update()
            
        except Exception as e:
            print(f"Home Page Error: {e}")
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"خطأ: {e}", color="#ff0000"),
                            ft.ElevatedButton("إعادة المحاولة", on_click=lambda e: show_home_page()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                )
            )
            page.update()
    
    def show_adhkar_page(category_id, category_name):
        """عرض صفحة الأذكار"""
        try:
            adhkar = get_adhkar_by_category(category_id)
            categories = get_categories()
            category_color = PRIMARY_COLOR
            
            for cat in categories:
                if cat[0] == category_id:
                    category_color = cat[3]
                    break
            
            def reset_all(e):
                reset_adhkar_counts(category_id)
                show_adhkar_page(category_id, category_name)
            
            content_list = [
                create_header(category_name, show_back=True, show_settings=False),
                
                # زر إعادة التعيين
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="إعادة تعيين",
                                icon="refresh",
                                on_click=reset_all,
                                bgcolor=category_color,
                                color="#FFFFFF",
                            ),
                            ft.Text(
                                f"{len(adhkar)} ذكر",
                                size=state["font_size"] - 3,
                                color=get_secondary_text_color(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=10),
                ),
            ]
            
            # إضافة بطاقات الأذكار
            for d in adhkar:
                content_list.append(create_adhkar_card(d, category_color))
            
            content_list.append(ft.Container(height=20))
            
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        controls=content_list,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                    ),
                    bgcolor=get_bg_color(),
                    expand=True,
                )
            )
            page.update()
            
        except Exception as e:
            print(f"Adhkar Page Error: {e}")
    
    def show_tasbih_page(tasbih_id, name, count, target):
        """عرض صفحة عداد التسبيح"""
        try:
            state["current_tasbih_count"] = count
            state["current_tasbih_target"] = target
            
            count_display = ft.Text(
                str(state["current_tasbih_count"]),
                size=64,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR,
            )
            
            progress_value = min(state["current_tasbih_count"] / target, 1.0) if target > 0 else 0
            
            progress_ring = ft.ProgressRing(
                value=progress_value,
                width=200,
                height=200,
                stroke_width=10,
                color=PRIMARY_COLOR,
                bgcolor="#e0e0e0" if not state["dark_mode"] else "#404040",
            )
            
            def increment(e):
                state["current_tasbih_count"] += 1
                count_display.value = str(state["current_tasbih_count"])
                progress_ring.value = min(state["current_tasbih_count"] / target, 1.0) if target > 0 else 0
                update_tasbih_count(tasbih_id, state["current_tasbih_count"])
                page.update()
            
            def reset(e):
                state["current_tasbih_count"] = 0
                count_display.value = "0"
                progress_ring.value = 0
                reset_tasbih_count(tasbih_id)
                page.update()
            
            counter_area = ft.Container(
                content=ft.Stack(
                    controls=[
                        progress_ring,
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    count_display,
                                    ft.Text(
                                        f"الهدف: {target}",
                                        size=state["font_size"] - 2,
                                        color=get_secondary_text_color(),
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=4,
                            ),
                            width=200,
                            height=200,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    width=200,
                    height=200,
                ),
                on_click=increment,
                border_radius=100,
            )
            
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            create_header("التسبيح", show_back=True, show_settings=False),
                            
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Container(height=20),
                                        
                                        ft.Text(
                                            name,
                                            size=state["font_size"] + 6,
                                            weight=ft.FontWeight.BOLD,
                                            color=get_text_color(),
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        
                                        ft.Container(height=30),
                                        
                                        counter_area,
                                        
                                        ft.Container(height=16),
                                        
                                        ft.Text(
                                            "اضغط على الدائرة للتسبيح",
                                            size=state["font_size"] - 3,
                                            color=get_secondary_text_color(),
                                        ),
                                        
                                        ft.Container(height=30),
                                        
                                        ft.ElevatedButton(
                                            text="إعادة تعيين",
                                            icon="refresh",
                                            on_click=reset,
                                            bgcolor="#ef4444",
                                            color="#FFFFFF",
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0,
                                ),
                                expand=True,
                                padding=16,
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=get_bg_color(),
                    expand=True,
                )
            )
            page.update()
            
        except Exception as e:
            print(f"Tasbih Page Error: {e}")
    
    def show_settings_page():
        """عرض صفحة الإعدادات"""
        try:
            font_preview = ft.Text(
                f"معاينة: حجم الخط {state['font_size']}",
                size=state["font_size"],
                color=get_text_color(),
            )
            
            def toggle_dark(e):
                state["dark_mode"] = e.control.value
                save_setting("dark_mode", "true" if state["dark_mode"] else "false")
                page.theme_mode = ft.ThemeMode.DARK if state["dark_mode"] else ft.ThemeMode.LIGHT
                page.update()
                show_settings_page()
            
            def change_font(e):
                state["font_size"] = int(e.control.value)
                save_setting("font_size", str(state["font_size"]))
                font_preview.value = f"معاينة: حجم الخط {state['font_size']}"
                font_preview.size = state["font_size"]
                page.update()
            
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            create_header("الإعدادات", show_back=True, show_settings=False),
                            
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        # الوضع الداكن
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Icon(
                                                                name="dark_mode" if state["dark_mode"] else "light_mode",
                                                                color=PRIMARY_COLOR,
                                                                size=24,
                                                            ),
                                                            ft.Text(
                                                                "الوضع الداكن",
                                                                size=state["font_size"],
                                                                color=get_text_color(),
                                                            ),
                                                        ],
                                                        spacing=12,
                                                    ),
                                                    ft.Switch(
                                                        value=state["dark_mode"],
                                                        active_color=PRIMARY_COLOR,
                                                        on_change=toggle_dark,
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            ),
                                            padding=16,
                                            border_radius=10,
                                            bgcolor=get_card_color(),
                                        ),
                                        
                                        ft.Container(height=12),
                                        
                                        # حجم الخط
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Icon(
                                                                name="text_fields",
                                                                color=PRIMARY_COLOR,
                                                                size=24,
                                                            ),
                                                            ft.Text(
                                                                "حجم الخط",
                                                                size=state["font_size"],
                                                                color=get_text_color(),
                                                            ),
                                                        ],
                                                        spacing=12,
                                                    ),
                                                    ft.Slider(
                                                        min=14,
                                                        max=26,
                                                        value=state["font_size"],
                                                        divisions=12,
                                                        active_color=PRIMARY_COLOR,
                                                        on_change=change_font,
                                                    ),
                                                    font_preview,
                                                ],
                                                spacing=8,
                                            ),
                                            padding=16,
                                            border_radius=10,
                                            bgcolor=get_card_color(),
                                        ),
                                        
                                        ft.Container(height=24),
                                        
                                        # معلومات التطبيق
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    ft.Text("🕌", size=36),
                                                    ft.Text(
                                                        "حصن المسلم",
                                                        size=state["font_size"] + 2,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=get_text_color(),
                                                    ),
                                                    ft.Text(
                                                        "الإصدار 1.0.0",
                                                        size=state["font_size"] - 3,
                                                        color=get_secondary_text_color(),
                                                    ),
                                                    ft.Text(
                                                        "أذكار من الكتاب والسنة",
                                                        size=state["font_size"] - 3,
                                                        color=get_secondary_text_color(),
                                                    ),
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                spacing=4,
                                            ),
                                            padding=24,
                                            border_radius=10,
                                            bgcolor=get_card_color(),
                                            alignment=ft.alignment.center,
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                padding=12,
                                expand=True,
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                    ),
                    bgcolor=get_bg_color(),
                    expand=True,
                )
            )
            page.update()
            
        except Exception as e:
            print(f"Settings Error: {e}")
    
    # بدء التطبيق
    try:
        setup_page()
        show_home_page()
    except Exception as e:
        print(f"App Error: {e}")
        page.add(ft.Text(f"خطأ في التطبيق: {e}", color="#ff0000"))
        page.update()

# تشغيل التطبيق
if __name__ == "__main__":
    ft.app(target=main)
