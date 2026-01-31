import flet as ft

def main(page: ft.Page):
    
    # إعدادات أساسية
    page.title = "حصن المسلم"
    page.rtl = True
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f5f5f5"
    
    # الألوان
    GREEN = "#10b981"
    
    # البيانات مباشرة في الكود
    categories_data = [
        {"id": 1, "name": "أذكار الصباح", "icon": "sunny", "color": "#10b981"},
        {"id": 2, "name": "أذكار المساء", "icon": "nights_stay", "color": "#6366f1"},
        {"id": 3, "name": "أذكار الصلاة", "icon": "favorite", "color": "#f59e0b"},
        {"id": 4, "name": "أذكار النوم", "icon": "bedtime", "color": "#8b5cf6"},
        {"id": 5, "name": "أذكار متنوعة", "icon": "star", "color": "#ec4899"},
    ]
    
    adhkar_data = {
        1: [
            {"text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ", "count": 1, "benefit": "ذكر الصباح"},
            {"text": "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", "count": 1, "benefit": "رواه الترمذي"},
            {"text": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ خَلَقْتَنِي وَأَنَا عَبْدُكَ", "count": 1, "benefit": "سيد الاستغفار"},
            {"text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "count": 100, "benefit": "مائة مرة"},
            {"text": "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "count": 10, "benefit": "عشر مرات"},
            {"text": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", "count": 3, "benefit": "ثلاث مرات"},
            {"text": "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", "count": 3, "benefit": "ثلاث مرات"},
        ],
        2: [
            {"text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ", "count": 1, "benefit": "ذكر المساء"},
            {"text": "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ", "count": 1, "benefit": "رواه الترمذي"},
            {"text": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", "count": 3, "benefit": "ثلاث مرات"},
            {"text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "count": 100, "benefit": "مائة مرة"},
        ],
        3: [
            {"text": "أَسْتَغْفِرُ اللَّهَ أَسْتَغْفِرُ اللَّهَ أَسْتَغْفِرُ اللَّهَ", "count": 3, "benefit": "بعد الصلاة"},
            {"text": "اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ", "count": 1, "benefit": "بعد الصلاة"},
            {"text": "سُبْحَانَ اللَّهِ", "count": 33, "benefit": "بعد الصلاة"},
            {"text": "الْحَمْدُ لِلَّهِ", "count": 33, "benefit": "بعد الصلاة"},
            {"text": "اللَّهُ أَكْبَرُ", "count": 33, "benefit": "بعد الصلاة"},
        ],
        4: [
            {"text": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", "count": 1, "benefit": "عند النوم"},
            {"text": "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ", "count": 1, "benefit": "عند النوم"},
            {"text": "سُبْحَانَ اللَّهِ", "count": 33, "benefit": "قبل النوم"},
            {"text": "الْحَمْدُ لِلَّهِ", "count": 33, "benefit": "قبل النوم"},
            {"text": "اللَّهُ أَكْبَرُ", "count": 34, "benefit": "قبل النوم"},
        ],
        5: [
            {"text": "لَا إِلَهَ إِلَّا اللَّهُ", "count": 100, "benefit": "أفضل الذكر"},
            {"text": "سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ", "count": 100, "benefit": "الباقيات الصالحات"},
            {"text": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", "count": 100, "benefit": "كنز من الجنة"},
            {"text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ سُبْحَانَ اللَّهِ الْعَظِيمِ", "count": 100, "benefit": "ثقيلتان في الميزان"},
            {"text": "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ", "count": 100, "benefit": "الصلاة على النبي"},
        ],
    }
    
    tasbih_data = [
        {"id": 1, "name": "سُبْحَانَ اللَّهِ", "count": 0, "target": 33},
        {"id": 2, "name": "الْحَمْدُ لِلَّهِ", "count": 0, "target": 33},
        {"id": 3, "name": "اللَّهُ أَكْبَرُ", "count": 0, "target": 34},
        {"id": 4, "name": "لَا إِلَهَ إِلَّا اللَّهُ", "count": 0, "target": 100},
        {"id": 5, "name": "أَسْتَغْفِرُ اللَّهَ", "count": 0, "target": 100},
    ]
    
    # حالة العدادات
    adhkar_counters = {}
    tasbih_counters = {t["id"]: t["count"] for t in tasbih_data}
    
    # ==================== الصفحة الرئيسية ====================
    
    def show_home():
        
        def open_category(e):
            cat_id = e.control.data["id"]
            cat_name = e.control.data["name"]
            cat_color = e.control.data["color"]
            show_adhkar(cat_id, cat_name, cat_color)
        
        def open_tasbih(e):
            t_data = e.control.data
            show_tasbih_page(t_data)
        
        def open_settings(e):
            show_settings()
        
        # بناء بطاقات الفئات
        cat_cards = []
        for cat in categories_data:
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(cat["icon"], size=30, color="#ffffff"),
                            width=55,
                            height=55,
                            border_radius=27,
                            bgcolor=cat["color"],
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(
                            cat["name"],
                            size=14,
                            color="#333333",
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                width=140,
                height=120,
                border_radius=12,
                bgcolor="#ffffff",
                padding=10,
                data=cat,
                on_click=open_category,
            )
            cat_cards.append(card)
        
        # بناء عناصر التسبيح
        tasbih_items = []
        for t in tasbih_data:
            item = ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                str(tasbih_counters.get(t["id"], 0)),
                                size=14,
                                color=GREEN,
                                weight=ft.FontWeight.BOLD,
                            ),
                            width=42,
                            height=42,
                            border_radius=21,
                            bgcolor="#e8f5e9",
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text(t["name"], size=14, color="#333333", weight=ft.FontWeight.W_500),
                                ft.Text(f"{tasbih_counters.get(t['id'], 0)} / {t['target']}", size=11, color="#888888"),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon("chevron_left", color="#888888", size=18),
                    ],
                    spacing=10,
                ),
                padding=10,
                border_radius=8,
                bgcolor="#ffffff",
                margin=ft.margin.only(bottom=6, left=10, right=10),
                data=t,
                on_click=open_tasbih,
            )
            tasbih_items.append(item)
        
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(width=40),
                                ft.Text(
                                    "حصن المسلم",
                                    size=18,
                                    color="#ffffff",
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.IconButton(
                                    icon="settings",
                                    icon_color="#ffffff",
                                    icon_size=20,
                                    on_click=open_settings,
                                ),
                            ],
                        ),
                        padding=10,
                        bgcolor=GREEN,
                    ),
                    
                    # المحتوى
                    ft.Container(
                        content=ft.Column(
                            [
                                # البطاقة الترحيبية
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
                                                size=16,
                                                color="#ffffff",
                                                weight=ft.FontWeight.BOLD,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                            ft.Text(
                                                "أذكار من الكتاب والسنة",
                                                size=12,
                                                color="#e0e0e0",
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=4,
                                    ),
                                    padding=16,
                                    margin=10,
                                    border_radius=10,
                                    bgcolor=GREEN,
                                ),
                                
                                # عنوان الأقسام
                                ft.Container(
                                    content=ft.Text(
                                        "أقسام الأذكار",
                                        size=15,
                                        color="#333333",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    padding=ft.padding.only(right=12, top=6, bottom=6),
                                ),
                                
                                # شبكة الفئات
                                ft.Container(
                                    content=ft.Row(
                                        controls=cat_cards,
                                        wrap=True,
                                        spacing=8,
                                        run_spacing=8,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.symmetric(horizontal=8),
                                ),
                                
                                # عنوان التسبيح
                                ft.Container(
                                    content=ft.Text(
                                        "التسبيح الإلكتروني",
                                        size=15,
                                        color="#333333",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    padding=ft.padding.only(right=12, top=12, bottom=6),
                                ),
                                
                                # قائمة التسبيحات
                                ft.Column(controls=tasbih_items, spacing=0),
                                
                                ft.Container(height=16),
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            spacing=0,
                        ),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
        page.update()
    
    # ==================== صفحة الأذكار ====================
    
    def show_adhkar(cat_id, cat_name, cat_color):
        
        adhkar_list = adhkar_data.get(cat_id, [])
        
        # تهيئة العدادات إذا لم تكن موجودة
        if cat_id not in adhkar_counters:
            adhkar_counters[cat_id] = [0] * len(adhkar_list)
        
        def go_back(e):
            show_home()
        
        def reset_all(e):
            adhkar_counters[cat_id] = [0] * len(adhkar_list)
            show_adhkar(cat_id, cat_name, cat_color)
        
        # بناء بطاقات الأذكار
        cards = []
        for idx, dhikr in enumerate(adhkar_list):
            current = adhkar_counters[cat_id][idx]
            remaining = max(0, dhikr["count"] - current)
            done = remaining == 0
            
            btn_text = ft.Text(
                "✓" if done else str(remaining),
                size=18,
                color="#ffffff",
                weight=ft.FontWeight.BOLD,
            )
            
            count_btn = ft.Container(
                content=btn_text,
                width=48,
                height=48,
                border_radius=24,
                bgcolor="#22c55e" if done else cat_color,
                alignment=ft.alignment.center,
                data={"idx": idx, "total": dhikr["count"]},
            )
            
            def make_tap_handler(index, total, button, text_widget):
                def handler(e):
                    curr = adhkar_counters[cat_id][index]
                    if curr < total:
                        adhkar_counters[cat_id][index] = curr + 1
                        rem = total - adhkar_counters[cat_id][index]
                        if rem == 0:
                            button.bgcolor = "#22c55e"
                            text_widget.value = "✓"
                        else:
                            text_widget.value = str(rem)
                        page.update()
                return handler
            
            count_btn.on_click = make_tap_handler(idx, dhikr["count"], count_btn, btn_text)
            
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            dhikr["text"],
                            size=15,
                            color="#333333",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(color="#e0e0e0"),
                        ft.Row(
                            [
                                count_btn,
                                ft.Column(
                                    [
                                        ft.Text(f"العدد: {dhikr['count']}", size=12, color="#888888"),
                                        ft.Text(dhikr["benefit"], size=11, color=cat_color),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=14,
                        ),
                    ],
                    spacing=8,
                ),
                padding=14,
                margin=ft.margin.only(bottom=8, left=10, right=10),
                border_radius=10,
                bgcolor="#ffffff",
            )
            cards.append(card)
        
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon="arrow_forward",
                                    icon_color="#ffffff",
                                    icon_size=20,
                                    on_click=go_back,
                                ),
                                ft.Text(
                                    cat_name,
                                    size=16,
                                    color="#ffffff",
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Container(width=40),
                            ],
                        ),
                        padding=10,
                        bgcolor=cat_color,
                    ),
                    
                    # زر إعادة التعيين
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.TextButton(
                                    text="إعادة تعيين",
                                    icon="refresh",
                                    on_click=reset_all,
                                ),
                                ft.Text(f"{len(adhkar_list)} ذكر", size=12, color="#888888"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=10,
                    ),
                    
                    # قائمة الأذكار
                    ft.Container(
                        content=ft.Column(
                            controls=cards,
                            scroll=ft.ScrollMode.AUTO,
                            spacing=0,
                        ),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
        page.update()
    
    # ==================== صفحة التسبيح ====================
    
    def show_tasbih_page(t_data):
        t_id = t_data["id"]
        t_name = t_data["name"]
        t_target = t_data["target"]
        
        count_val = tasbih_counters.get(t_id, 0)
        
        count_text = ft.Text(
            str(count_val),
            size=50,
            color=GREEN,
            weight=ft.FontWeight.BOLD,
        )
        
        progress = ft.ProgressRing(
            value=min(count_val / t_target, 1.0) if t_target > 0 else 0,
            width=160,
            height=160,
            stroke_width=8,
            color=GREEN,
            bgcolor="#e0e0e0",
        )
        
        def go_back(e):
            show_home()
        
        def increment(e):
            tasbih_counters[t_id] = tasbih_counters.get(t_id, 0) + 1
            count_text.value = str(tasbih_counters[t_id])
            progress.value = min(tasbih_counters[t_id] / t_target, 1.0) if t_target > 0 else 0
            page.update()
        
        def reset(e):
            tasbih_counters[t_id] = 0
            count_text.value = "0"
            progress.value = 0
            page.update()
        
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon="arrow_forward",
                                    icon_color="#ffffff",
                                    icon_size=20,
                                    on_click=go_back,
                                ),
                                ft.Text(
                                    "التسبيح",
                                    size=16,
                                    color="#ffffff",
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Container(width=40),
                            ],
                        ),
                        padding=10,
                        bgcolor=GREEN,
                    ),
                    
                    # المحتوى
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(height=20),
                                
                                ft.Text(
                                    t_name,
                                    size=22,
                                    color="#333333",
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                
                                ft.Container(height=30),
                                
                                # العداد الدائري
                                ft.GestureDetector(
                                    content=ft.Stack(
                                        [
                                            progress,
                                            ft.Container(
                                                content=ft.Column(
                                                    [
                                                        count_text,
                                                        ft.Text(
                                                            f"الهدف: {t_target}",
                                                            size=12,
                                                            color="#888888",
                                                        ),
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                ),
                                                width=160,
                                                height=160,
                                                alignment=ft.alignment.center,
                                            ),
                                        ],
                                        width=160,
                                        height=160,
                                    ),
                                    on_tap=increment,
                                ),
                                
                                ft.Container(height=16),
                                
                                ft.Text(
                                    "اضغط على الدائرة للتسبيح",
                                    size=13,
                                    color="#888888",
                                ),
                                
                                ft.Container(height=30),
                                
                                ft.ElevatedButton(
                                    text="إعادة تعيين",
                                    icon="refresh",
                                    on_click=reset,
                                    bgcolor="#ef4444",
                                    color="#ffffff",
                                ),
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
    
    def show_settings():
        
        def go_back(e):
            show_home()
        
        def toggle_theme(e):
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                page.bgcolor = "#1e1e2e"
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.bgcolor = "#f5f5f5"
            show_settings()
        
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        colors = {
            "bg": "#1e1e2e" if is_dark else "#f5f5f5",
            "card": "#2d2d3f" if is_dark else "#ffffff",
            "text": "#ffffff" if is_dark else "#333333",
            "subtext": "#a0a0a0" if is_dark else "#888888",
        }
        
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    # الهيدر
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon="arrow_forward",
                                    icon_color="#ffffff",
                                    icon_size=20,
                                    on_click=go_back,
                                ),
                                ft.Text(
                                    "الإعدادات",
                                    size=16,
                                    color="#ffffff",
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Container(width=40),
                            ],
                        ),
                        padding=10,
                        bgcolor=GREEN,
                    ),
                    
                    ft.Container(
                        content=ft.Column(
                            [
                                # الوضع الداكن
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(
                                                "dark_mode" if is_dark else "light_mode",
                                                color=GREEN,
                                                size=22,
                                            ),
                                            ft.Text(
                                                "الوضع الداكن",
                                                size=15,
                                                color=colors["text"],
                                            ),
                                            ft.Container(expand=True),
                                            ft.Switch(
                                                value=is_dark,
                                                active_color=GREEN,
                                                on_change=toggle_theme,
                                            ),
                                        ],
                                    ),
                                    padding=14,
                                    border_radius=8,
                                    bgcolor=colors["card"],
                                ),
                                
                                ft.Container(height=20),
                                
                                # معلومات التطبيق
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Icon("menu_book", color=GREEN, size=40),
                                            ft.Text(
                                                "حصن المسلم",
                                                size=18,
                                                color=colors["text"],
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                "الإصدار 1.0",
                                                size=12,
                                                color=colors["subtext"],
                                            ),
                                            ft.Text(
                                                "أذكار من الكتاب والسنة",
                                                size=12,
                                                color=colors["subtext"],
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=4,
                                    ),
                                    padding=20,
                                    border_radius=8,
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
    show_home()


ft.app(target=main)
