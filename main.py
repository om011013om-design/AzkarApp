import flet as ft
import sqlite3
import os

# ==========================================
# 1. إعدادات البيانات والخط
# ==========================================

# اسم ملف الخط كما رفعته (بصيغة OTF)
FONT_FILE_NAME = "myfont.otf"
FONT_NAME_INTERNAL = "ThuluthFont"

DEFAULT_CATEGORIES = {
    "morning": {"name": "أذكار الصباح", "icon": ft.icons.WB_SUNNY, "color": "#f59e0b"},
    "evening": {"name": "أذكار المساء", "icon": ft.icons.NIGHTS_STAY, "color": "#6366f1"},
    "prayer": {"name": "أذكار الصلاة", "icon": ft.icons.MOSQUE, "color": "#10b981"},
    "sleep": {"name": "أذكار النوم", "icon": ft.icons.BEDTIME, "color": "#8b5cf6"},
    "tasbih": {"name": "التسبيح العام", "icon": ft.icons.FAVORITE, "color": "#ef4444"},
    "waking": {"name": "أذكار الاستيقاظ", "icon": ft.icons.ALARM, "color": "#14b8a6"},
    "food": {"name": "أذكار الطعام", "icon": ft.icons.RESTAURANT, "color": "#f97316"},
    "travel": {"name": "أذكار السفر", "icon": ft.icons.FLIGHT, "color": "#0ea5e9"},
    "quran": {"name": "أدعية قرآنية", "icon": ft.icons.MENU_BOOK, "color": "#10b981"}
}

DEFAULT_AZKAR = {
    "morning": [
        {"text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ.", "count": 1, "benefit": "من قالها حين يصبح فقد أدى شكر يومه"},
        {"text": "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ.", "count": 1, "benefit": "دعاء الصباح"},
        {"text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ.", "count": 100, "benefit": "حطت خطاياه وإن كانت مثل زبد البحر"},
        {"text": "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ.", "count": 100, "benefit": "تكفير الذنوب وتفريج الهموم"}
    ],
    "evening": [
        {"text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ.", "count": 1, "benefit": "من قالها حين يمسي فقد أدى شكر ليلته"},
        {"text": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ.", "count": 3, "benefit": "لم تضره حمة تلك الليلة"},
        {"text": "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ.", "count": 1, "benefit": "دعاء المساء"}
    ],
    "prayer": [
        {"text": "أَسْتَغْفِرُ اللَّهَ (ثلاثاً) اللَّهُمَّ أَنْتَ السَّلَامُ، وَمِنْكَ السَّلَامُ، تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ.", "count": 1, "benefit": "بعد السلام من الصلاة"},
        {"text": "سُبْحَانَ اللَّهِ (33)، الْحَمْدُ لِلَّهِ (33)، اللَّهُ أَكْبَرُ (33)، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ.", "count": 1, "benefit": "من قالها غفرت خطاياه"}
    ],
    "sleep": [
        {"text": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا.", "count": 1, "benefit": "عند النوم"},
        {"text": "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ.", "count": 3, "benefit": "وقاية من العذاب"},
        {"text": "سُبْحَانَ اللَّهِ (33) وَالْحَمْدُ لِلَّهِ (33) وَاللَّهُ أَكْبَرُ (34).", "count": 1, "benefit": "أوصى بها النبي ﷺ لفاطمة"}
    ],
     "tasbih": [
        {"text": "سُبْحَانَ اللَّهِ.", "count": 100, "benefit": "أجر عظيم"},
        {"text": "الْحَمْدُ لِلَّهِ.", "count": 100, "benefit": "تملأ الميزان"},
        {"text": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ.", "count": 100, "benefit": "كنز من كنوز الجنة"},
        {"text": "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَىٰ نَبِيِّنَا مُحَمَّدٍ.", "count": 10, "benefit": "من صلى علي واحدة صلى الله عليه بها عشراً"}
    ],
    "waking": [
        {"text": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ.", "count": 1, "benefit": "عند الاستيقاظ"}
    ],
    "food": [
        {"text": "بِسْمِ اللَّهِ.", "count": 1, "benefit": "قبل الأكل"},
        {"text": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَٰذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ.", "count": 1, "benefit": "غفر له ما تقدم من ذنبه"}
    ],
    "travel": [
        {"text": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَٰذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ.", "count": 1, "benefit": "دعاء السفر"}
    ],
    "quran": [
        {"text": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ.", "count": 1, "benefit": "أكثر دعاء النبي ﷺ"}
    ]
}

# ==========================================
# 2. قاعدة البيانات (DATABASE)
# ==========================================

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("hisn_app.db", check_same_thread=False)
        self.create_tables()
        self.init_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasbih_stats (total INTEGER DEFAULT 0)''')
        self.conn.commit()

    def init_data(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('font_size', '28')") # كبرنا الخط الافتراضي عشان الثلث يبان
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('dark_mode', '0')")
        cursor.execute("INSERT OR IGNORE INTO tasbih_stats (total) VALUES (0)")
        self.conn.commit()

    def get_setting(self, key):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        res = cursor.fetchone()
        return res[0] if res else None

    def set_setting(self, key, value):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def update_tasbih(self, count):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasbih_stats SET total = total + ?", (count,))
        self.conn.commit()

    def get_tasbih_total(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT total FROM tasbih_stats")
        res = cursor.fetchone()
        return res[0] if res else 0

# ==========================================
# 3. التطبيق (UI & LOGIC)
# ==========================================

def main(page: ft.Page):
    # إعدادات الصفحة
    page.title = "حصن المسلم"
    page.rtl = True
    page.padding = 0
    page.scroll = "adaptive"

    # ==============================
    # 🎨 إعداد خط الثلث هنا
    # ==============================
    page.fonts = {
        FONT_NAME_INTERNAL: FONT_FILE_NAME
    }
    page.theme = ft.Theme(font_family=FONT_NAME_INTERNAL)
    
    # تهيئة قاعدة البيانات والإعدادات
    db = Database()
    current_font_size = int(db.get_setting('font_size'))
    is_dark = db.get_setting('dark_mode') == '1'
    page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
    
    tasbih_counter_val = 0
    
    # --- الدوال المساعدة ---
    
    def toggle_theme(e):
        nonlocal is_dark
        is_dark = not is_dark
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        db.set_setting('dark_mode', '1' if is_dark else '0')
        page.update()

    def change_font_size(e):
        nonlocal current_font_size
        current_font_size = int(e.control.value)
        db.set_setting('font_size', str(current_font_size))
        page.snack_bar = ft.SnackBar(ft.Text("تم حفظ الحجم، سيطبق عند فتح الأذكار"))
        page.snack_bar.open = True
        page.update()

    # --- الصفحات ---

    def build_home():
        # كروت الفئات
        cards = []
        for cat_key, cat_data in DEFAULT_CATEGORIES.items():
            cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(cat_data['icon'], size=40, color="white"),
                        ft.Text(cat_data['name'], size=20, weight="bold", color="white") # تكبير بسيط
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=cat_data['color'],
                    border_radius=15,
                    padding=20,
                    ink=True,
                    on_click=lambda e, k=cat_key: open_azkar_category(k),
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.3, "black")),
                    height=130,
                )
            )
        
        # تخطيط الشبكة
        grid = ft.ResponsiveRow(
            [ft.Column(col={"xs": 6}, controls=[c]) for c in cards],
            run_spacing=15,
            spacing=15
        )

        return ft.View(
            "/",
            controls=[
                ft.AppBar(
                    title=ft.Text("حصن المسلم", weight="bold"),
                    center_title=True,
                    bgcolor="#10b981",
                    color="white",
                    actions=[
                        ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=toggle_theme, tooltip="الوضع الليلي"),
                    ]
                ),
                ft.Container(
                    content=grid,
                    padding=20,
                ),
                ft.FloatingActionButton(
                    icon=ft.icons.FINGERPRINT,
                    bgcolor="#10b981",
                    text="المسبحة",
                    on_click=lambda _: page.go("/tasbih")
                )
            ],
            bgcolor=ft.colors.BACKGROUND
        )

    def open_azkar_category(category_key):
        azkar_list = DEFAULT_AZKAR.get(category_key, [])
        cat_info = DEFAULT_CATEGORIES.get(category_key)
        
        def build_zikr_card(zikr):
            count_remaining = zikr['count']
            
            count_btn = ft.ElevatedButton(
                text=str(count_remaining),
                bgcolor=cat_info['color'],
                color="white",
                width=60,
                height=60,
                style=ft.ButtonStyle(shape=ft.CircleBorder())
            )
            
            def decrement(e):
                nonlocal count_remaining
                if count_remaining > 0:
                    count_remaining -= 1
                    count_btn.text = str(count_remaining)
                    if count_remaining == 0:
                        count_btn.bgcolor = "grey"
                        count_btn.text = "✓"
                        e.control.parent.parent.bgcolor = ft.colors.with_opacity(0.1, "green")
                    e.control.update()
                    e.control.parent.parent.update()

            count_btn.on_click = decrement

            return ft.Container(
                content=ft.Column([
                    ft.Text(zikr['text'], size=current_font_size, text_align="center", selectable=True),
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([
                        ft.Text(zikr['benefit'], size=14, color="grey", expand=True),
                        count_btn
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ]),
                padding=20,
                border_radius=10,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border=ft.border.all(1, ft.colors.OUTLINE_VARIANT)
            )

        page.views.append(
            ft.View(
                f"/azkar/{category_key}",
                controls=[
                    ft.AppBar(title=ft.Text(cat_info['name']), bgcolor=cat_info['color'], color="white"),
                    ft.ListView(
                        controls=[build_zikr_card(z) for z in azkar_list],
                        expand=True,
                        spacing=10,
                        padding=15
                    )
                ]
            )
        )
        page.update()

    def build_tasbih_view():
        nonlocal tasbih_counter_val
        tasbih_counter_val = 0
        total_global = db.get_tasbih_total()
        
        counter_display = ft.Text("0", size=100, weight="bold", color="#10b981") # تكبير العداد
        total_display = ft.Text(f"مجموع تسبيحاتك الكلي: {total_global}", size=18, color="grey")

        def click_tasbih(e):
            nonlocal tasbih_counter_val
            tasbih_counter_val += 1
            counter_display.value = str(tasbih_counter_val)
            if tasbih_counter_val % 5 == 0:
                db.update_tasbih(5)
                total_display.value = f"مجموع تسبيحاتك الكلي: {db.get_tasbih_total()}"
            page.update()

        def save_and_exit(e):
            remainder = tasbih_counter_val % 5
            if remainder > 0:
                db.update_tasbih(remainder)
            page.views.pop()
            page.go("/")

        return ft.View(
            "/tasbih",
            controls=[
                ft.AppBar(
                    title=ft.Text("المسبحة الإلكترونية"), 
                    bgcolor="#10b981", 
                    color="white",
                    leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=save_and_exit)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=50),
                        counter_display,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "سبحان الله", 
                            on_click=click_tasbih,
                            width=220, 
                            height=220,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                bgcolor="#10b981",
                                color="white",
                            )
                        ),
                        ft.Container(height=30),
                        total_display
                    ], horizontal_alignment="center"),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )

    def route_change(route):
        page.views.clear()
        page.views.append(build_home())
        if page.route == "/tasbih":
            page.views.append(build_tasbih_view())
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
