import flet as ft
import sqlite3
import os

# ==================== قاعدة البيانات ====================

DB_NAME = "adhkar.db"

def get_db_path():
    try:
        # للأندرويد
        if hasattr(os, 'environ') and 'ANDROID_BOOTLOGO' in os.environ:
            return f"/data/data/com.example.app/{DB_NAME}"
        return DB_NAME
    except:
        return DB_NAME

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS categories
                     (id INTEGER PRIMARY KEY, name TEXT, icon TEXT, color TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS adhkar
                     (id INTEGER PRIMARY KEY, cat_id INTEGER, text TEXT, 
                      total INTEGER, current INTEGER, benefit TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS tasbih
                     (id INTEGER PRIMARY KEY, name TEXT, count INTEGER, target INTEGER)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS settings
                     (key TEXT PRIMARY KEY, value TEXT)''')
        
        # التحقق من وجود بيانات
        c.execute("SELECT COUNT(*) FROM categories")
        if c.fetchone()[0] == 0:
            # إدخال الفئات
            cats = [
                (1, "أذكار الصباح", "sunny", "#10b981"),
                (2, "أذكار المساء", "bedtime", "#6366f1"),
                (3, "أذكار الصلاة", "favorite", "#f59e0b"),
                (4, "أذكار النوم", "nights_stay", "#8b5cf6"),
                (5, "أذكار متنوعة", "star", "#ec4899"),
            ]
            c.executemany("INSERT INTO categories VALUES (?,?,?,?)", cats)
            
            # إدخال الأذكار
            adhkar_data = [
                # أذكار الصباح
                (1, 1, "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ", 1, 0, "ذكر الصباح"),
                (2, 1, "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", 1, 0, "رواه الترمذي"),
                (3, 1, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", 100, 0, "مائة مرة"),
                (4, 1, "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ", 10, 0, "عشر مرات"),
                (5, 1, "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", 3, 0, "ثلاث مرات"),
                
                # أذكار المساء
                (6, 2, "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ", 1, 0, "ذكر المساء"),
                (7, 2, "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ", 1, 0, "رواه الترمذي"),
                (8, 2, "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", 3, 0, "ثلاث مرات"),
                (9, 2, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", 100, 0, "مائة مرة"),
                
                # أذكار الصلاة
                (10, 3, "أَسْتَغْفِرُ اللَّهَ أَسْتَغْفِرُ اللَّهَ أَسْتَغْفِرُ اللَّهَ", 3, 0, "بعد الصلاة"),
                (11, 3, "سُبْحَانَ اللَّهِ", 33, 0, "بعد الصلاة"),
                (12, 3, "الْحَمْدُ لِلَّهِ", 33, 0, "بعد الصلاة"),
                (13, 3, "اللَّهُ أَكْبَرُ", 33, 0, "بعد الصلاة"),
                
                # أذكار النوم
                (14, 4, "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", 1, 0, "عند النوم"),
                (15, 4, "سُبْحَانَ اللَّهِ", 33, 0, "قبل النوم"),
                (16, 4, "الْحَمْدُ لِلَّهِ", 33, 0, "قبل النوم"),
                (17, 4, "اللَّهُ أَكْبَرُ", 34, 0, "قبل النوم"),
                
                # أذكار متنوعة
                (18, 5, "لَا إِلَهَ إِلَّا اللَّهُ", 100, 0, "أفضل الذكر"),
                (19, 5, "سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ", 100, 0, "الباقيات الصالحات"),
                (20, 5, "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", 100, 0, "كنز من الجنة"),
            ]
            c.executemany("INSERT INTO adhkar VALUES (?,?,?,?,?,?)", adhkar_data)
            
            # إدخال التسبيحات
            tasbih_data = [
                (1, "سُبْحَانَ اللَّهِ", 0, 33),
                (2, "الْحَمْدُ لِلَّهِ", 0, 33),
                (3, "اللَّهُ أَكْبَرُ", 0, 34),
                (4, "لَا إِلَهَ إِلَّا اللَّهُ", 0, 100),
                (5, "أَسْتَغْفِرُ اللَّهَ", 0, 100),
            ]
            c.executemany("INSERT INTO tasbih VALUES (?,?,?,?)", tasbih_data)
            
            # الإعدادات
            c.execute("INSERT OR REPLACE INTO settings VALUES ('dark_mode', 'false')")
            c.execute("INSERT OR REPLACE INTO settings VALUES ('font_size', '18')")
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def db_query(query, params=(), fetch=True):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(query, params)
        if fetch:
            result = c.fetchall()
        else:
            conn.commit()
            result = True
        conn.close()
        return result
    except Exception as e:
        print(f"Query Error: {e}")
        return [] if fetch else False

# ==================== التطبيق ====================

def main(page: ft.Page):
    
    # الألوان
    GREEN = "#10b981"
    DARK_GREEN = "#059669"
    
    # المتغيرات
    dark_mode = False
    font_size = 18
    current_page = "home"
    
    # إعداد الصفحة
    page.title = "حصن المسلم"
    page.rtl = True
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # تهيئة قاعدة البيانات
    init_db()
    
    # تحميل الإعدادات
    try:
        result = db_query("SELECT value FROM settings WHERE key='dark_mode'")
        if result:
            dark_mode = result[0][0] == "true"
            page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT
        
        result = db_query("SELECT value FROM settings WHERE key='font_size'")
        if result:
            font_size = int(result[0][0])
    except:
        pass
    
    def get_colors():
        if dark_mode:
            return {"bg": "#1e1e2e", "card": "#2d2d3f", "text": "#ffffff", "subtext": "#a0a0a0"}
        else:
            return {"bg": "#f5f5f5", "card": "#ffffff", "text": "#000000", "subtext": "#666666"}
    
    # ==================== الصفحة الرئيسية ====================
    
    def build_home():
        colors = get_colors()
        
        # جلب الفئات
        categories = db_query("SELECT * FROM categories")
        
        # جلب التسبيحات
        tasbihat = db_query("SELECT * FROM tasbih")
        
        def open_category(cat_id, cat_name, cat_color):
            build_adhkar_page(cat_id, cat_name, cat_color)
        
        def open_tasbih(t_id, t_name, t_count, t_target):
            build_tasbih_page(t_id, t_name, t_count, t_target)
        
        def open_settings(e):
            build_settings()
        
        # بناء بطاقات الفئات
        cat_cards = []
        for cat in categories:
            cat_id, cat_name, cat_icon, cat_color = cat
            
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(cat_icon, size=32, color="#ffffff"),
                            width=60,
                            height=60,
                            border_radius=30,
                            bgcolor=cat_color,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(cat_name, size=font_size-2, color=colors["text"], 
                               text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                width=150,
                height=130,
                border_radius=12,
                bgcolor=colors["card"],
                padding=10,
                on_click=lambda e, cid=cat_id, cname=cat_name, ccol=cat_color: open_category(cid, cname, ccol),
            )
            cat_cards.append(card)
        
        # بناء قائمة التسبيحات
        tasbih_items = []
        for t in tasbihat:
            t_id, t_name, t_count, t_target = t
            
            item = ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(str(t_count), size=14, color=GREEN, weight=ft.FontWeight.BOLD),
                            width=45,
                            height=45,
                            border_radius=22,
                            bgcolor=colors["card"],
                            alignment=ft.alignment.center,
                            border=ft.border.all(2, GREEN),
                        ),
                        ft.Column(
                            [
                                ft.Text(t_name, size=font_size-2, color=colors["text"], weight=ft.FontWeight.W_500),
                                ft.Text(f"{t_count} / {t_target}", size=12, color=colors["subtext"]),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon("chevron_left", color=colors["subtext"], size=20),
                    ],
                    spacing=12,
                ),
                padding=12,
                border_radius=10,
                bgcolor=colors["card"],
                margin=ft.margin.only(bottom=8, left=12, right=12),
                on_click=lambda e, tid=t_id, tname=t_name, tc=t_count, tt=t_target: open_tasbih(tid, tname, tc, tt),
            )
            tasbih_items.append(item)
        
        # تجميع الصفحة
        page.controls.clear()
        page.bgcolor = colors["bg"]
        
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(width=40),
                                ft.Text("حصن المسلم", size=20, color="#ffffff", weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER),
                                ft.IconButton(icon="settings", icon_color="#ffffff", icon_size=22, on_click=open_settings),
                            ],
                        ),
                        padding=12,
                        bgcolor=GREEN,
                    ),
                    
                    # المحتوى
                    ft.Column(
                        [
                            # البطاقة الترحيبية
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", size=font_size+2, color="#ffffff", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                        ft.Text("أذكار من الكتاب والسنة", size=font_size-2, color="#e0e0e0", text_align=ft.TextAlign.CENTER),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=6,
                                ),
                                padding=20,
                                margin=12,
                                border_radius=12,
                                bgcolor=GREEN,
                            ),
                            
                            # عنوان الأقسام
                            ft.Container(
                                content=ft.Text("أقسام الأذكار", size=font_size, color=colors["text"], weight=ft.FontWeight.BOLD),
                                padding=ft.padding.only(right=16, top=8, bottom=8),
                            ),
                            
                            # شبكة الفئات
                            ft.Row(
                                controls=cat_cards,
                                wrap=True,
                                spacing=10,
                                run_spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            
                            # عنوان التسبيح
                            ft.Container(
                                content=ft.Text("التسبيح الإلكتروني", size=font_size, color=colors["text"], weight=ft.FontWeight.BOLD),
                                padding=ft.padding.only(right=16, top=16, bottom=8),
                            ),
                            
                            # قائمة التسبيحات
                            ft.Column(controls=tasbih_items, spacing=0),
                            
                            ft.Container(height=20),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
        page.update()
    
    # ==================== صفحة الأذكار ====================
    
    def build_adhkar_page(cat_id, cat_name, cat_color):
        colors = get_colors()
        
        adhkar = db_query("SELECT * FROM adhkar WHERE cat_id=?", (cat_id,))
        
        def go_back(e):
            build_home()
        
        def reset_all(e):
            db_query("UPDATE adhkar SET current=0 WHERE cat_id=?", (cat_id,), fetch=False)
            build_adhkar_page(cat_id, cat_name, cat_color)
        
        # بناء بطاقات الأذكار
        cards = []
        for dhikr in adhkar:
            d_id, d_cat, d_text, d_total, d_current, d_benefit = dhikr
            remaining = max(0, d_total - d_current)
            done = remaining == 0
            
            count_btn = ft.Container(
                content=ft.Text(
                    "✓" if done else str(remaining),
                    size=20,
                    color="#ffffff",
                    weight=ft.FontWeight.BOLD,
                ),
                width=50,
                height=50,
                border_radius=25,
                bgcolor="#22c55e" if done else cat_color,
                alignment=ft.alignment.center,
                data={"id": d_id, "total": d_total, "current": d_current},
            )
            
            def on_tap(e):
                data = e.control.data
                if data["current"] < data["total"]:
                    data["current"] += 1
                    db_query("UPDATE adhkar SET current=? WHERE id=?", (data["current"], data["id"]), fetch=False)
                    rem = data["total"] - data["current"]
                    if rem == 0:
                        e.control.bgcolor = "#22c55e"
                        e.control.content = ft.Text("✓", size=24, color="#ffffff", weight=ft.FontWeight.BOLD)
                    else:
                        e.control.content = ft.Text(str(rem), size=20, color="#ffffff", weight=ft.FontWeight.BOLD)
                    page.update()
            
            count_btn.on_click = on_tap
            
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(d_text, size=font_size, color=colors["text"], text_align=ft.TextAlign.CENTER),
                        ft.Divider(color=colors["subtext"]),
                        ft.Row(
                            [
                                count_btn,
                                ft.Column(
                                    [
                                        ft.Text(f"العدد: {d_total}", size=font_size-4, color=colors["subtext"]),
                                        ft.Text(d_benefit or "", size=font_size-5, color=cat_color),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=16,
                        ),
                    ],
                    spacing=10,
                ),
                padding=16,
                margin=ft.margin.only(bottom=10, left=12, right=12),
                border_radius=12,
                bgcolor=colors["card"],
            )
            cards.append(card)
        
        page.controls.clear()
        page.bgcolor = colors["bg"]
        
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(icon="arrow_forward", icon_color="#ffffff", icon_size=22, on_click=go_back),
                                ft.Text(cat_name, size=18, color="#ffffff", weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER),
                                ft.Container(width=40),
                            ],
                        ),
                        padding=12,
                        bgcolor=cat_color,
                    ),
                    
                    # زر إعادة التعيين
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.ElevatedButton("إعادة تعيين", icon="refresh", on_click=reset_all, bgcolor=cat_color, color="#ffffff"),
                                ft.Text(f"{len(adhkar)} ذكر", size=font_size-3, color=colors["subtext"]),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=12,
                    ),
                    
                    # قائمة الأذكار
                    ft.Column(
                        controls=cards,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
        page.update()
    
    # ==================== صفحة التسبيح ====================
    
    def build_tasbih_page(t_id, t_name, t_count, t_target):
        colors = get_colors()
        count = t_count
        
        def go_back(e):
            build_home()
        
        count_text = ft.Text(str(count), size=60, color=GREEN, weight=ft.FontWeight.BOLD)
        
        progress = ft.ProgressRing(
            value=min(count/t_target, 1.0) if t_target > 0 else 0,
            width=180,
            height=180,
            stroke_width=10,
            color=GREEN,
            bgcolor=colors["subtext"],
        )
        
        def increment(e):
            nonlocal count
            count += 1
            count_text.value = str(count)
            progress.value = min(count/t_target, 1.0) if t_target > 0 else 0
            db_query("UPDATE tasbih SET count=? WHERE id=?", (count, t_id), fetch=False)
            page.update()
        
        def reset(e):
            nonlocal count
            count = 0
            count_text.value = "0"
            progress.value = 0
            db_query("UPDATE tasbih SET count=0 WHERE id=?", (t_id,), fetch=False)
            page.update()
        
        page.controls.clear()
        page.bgcolor = colors["bg"]
        
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(icon="arrow_forward", icon_color="#ffffff", icon_size=22, on_click=go_back),
                                ft.Text("التسبيح", size=18, color="#ffffff", weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER),
                                ft.Container(width=40),
                            ],
                        ),
                        padding=12,
                        bgcolor=GREEN,
                    ),
                    
                    # المحتوى
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(height=20),
                                ft.Text(t_name, size=font_size+6, color=colors["text"], weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.Container(height=30),
                                
                                # العداد الدائري
                                ft.Container(
                                    content=ft.Stack(
                                        [
                                            progress,
                                            ft.Container(
                                                content=ft.Column(
                                                    [
                                                        count_text,
                                                        ft.Text(f"الهدف: {t_target}", size=14, color=colors["subtext"]),
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                ),
                                                width=180,
                                                height=180,
                                                alignment=ft.alignment.center,
                                            ),
                                        ],
                                        width=180,
                                        height=180,
                                    ),
                                    on_click=increment,
                                ),
                                
                                ft.Container(height=20),
                                ft.Text("اضغط على الدائرة للتسبيح", size=14, color=colors["subtext"]),
                                ft.Container(height=30),
                                
                                ft.ElevatedButton("إعادة تعيين", icon="refresh", on_click=reset, bgcolor="#ef4444", color="#ffffff"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
        page.update()
    
    # ==================== صفحة الإعدادات ====================
    
    def build_settings():
        nonlocal dark_mode, font_size
        colors = get_colors()
        
        def go_back(e):
            build_home()
        
        def toggle_dark(e):
            nonlocal dark_mode
            dark_mode = e.control.value
            db_query("UPDATE settings SET value=? WHERE key='dark_mode'", ("true" if dark_mode else "false",), fetch=False)
            page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT
            build_settings()
        
        def change_font(e):
            nonlocal font_size
            font_size = int(e.control.value)
            db_query("UPDATE settings SET value=? WHERE key='font_size'", (str(font_size),), fetch=False)
            preview.value = f"معاينة الخط: {font_size}"
            preview.size = font_size
            page.update()
        
        preview = ft.Text(f"معاينة الخط: {font_size}", size=font_size, color=colors["text"])
        
        page.controls.clear()
        page.bgcolor = colors["bg"]
        
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(icon="arrow_forward", icon_color="#ffffff", icon_size=22, on_click=go_back),
                                ft.Text("الإعدادات", size=18, color="#ffffff", weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER),
                                ft.Container(width=40),
                            ],
                        ),
                        padding=12,
                        bgcolor=GREEN,
                    ),
                    
                    ft.Container(
                        content=ft.Column(
                            [
                                # الوضع الداكن
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Text("الوضع الداكن", size=font_size, color=colors["text"]),
                                            ft.Switch(value=dark_mode, active_color=GREEN, on_change=toggle_dark),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    padding=16,
                                    border_radius=10,
                                    bgcolor=colors["card"],
                                ),
                                
                                ft.Container(height=12),
                                
                                # حجم الخط
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text("حجم الخط", size=font_size, color=colors["text"]),
                                            ft.Slider(min=14, max=24, value=font_size, divisions=10, active_color=GREEN, on_change=change_font),
                                            preview,
                                        ],
                                        spacing=8,
                                    ),
                                    padding=16,
                                    border_radius=10,
                                    bgcolor=colors["card"],
                                ),
                                
                                ft.Container(height=24),
                                
                                # معلومات
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text("حصن المسلم", size=font_size+2, color=colors["text"], weight=ft.FontWeight.BOLD),
                                            ft.Text("الإصدار 1.0", size=14, color=colors["subtext"]),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=4,
                                    ),
                                    padding=20,
                                    border_radius=10,
                                    bgcolor=colors["card"],
                                    alignment=ft.alignment.center,
                                ),
                            ],
                        ),
                        padding=12,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
        page.update()
    
    # بدء التطبيق
    build_home()

# تشغيل
ft.app(target=main)
