import flet as ft

def main(page: ft.Page):
    # 1. إعدادات التطبيق الاحترافية
    page.title = "المسبحة الإلكترونية"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    # ألوان التطبيق (أخضر إسلامي وهادئ)
    page.bgcolor = "#f0fdf4"  # خلفية فاتحة جداً
    page.scroll = "adaptive"

    # المتغير لحفظ الرقم
    count = 0

    # 2. واجهة الرقم (تصميم دائري فخم)
    txt_number = ft.Text(
        value="0",
        size=60,
        color="#15803d",  # أخضر غامق
        weight=ft.FontWeight.BOLD,
        font_family="Arial"
    )

    circle_container = ft.Container(
        content=txt_number,
        width=200,
        height=200,
        bgcolor="white",
        border_radius=100,  # دائرة كاملة
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.2, "green"),
        ),
        border=ft.border.all(5, "#bbf7d0"), # إطار أخضر فاتح
    )

    # 3. دوال الحركة (Logic)
    def plus_click(e):
        nonlocal count
        count += 1
        txt_number.value = str(count)
        page.update()

    def reset_click(e):
        nonlocal count
        count = 0
        txt_number.value = "0"
        page.update()

    # 4. الأزرار
    btn_tasbeeh = ft.ElevatedButton(
        text="تسبيح",
        width=150,
        height=50,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#16a34a", # أخضر زرعي
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=plus_click
    )

    btn_reset = ft.IconButton(
        icon=ft.icons.REFRESH,
        icon_color="#dc2626", # أحمر
        tooltip="تصفير",
        on_click=reset_click
    )

    # 5. التجميع النهائي
    page.appbar = ft.AppBar(
        title=ft.Text("ذكر الله", color="white", weight="bold"),
        center_title=True,
        bgcolor="#15803d",
    )

    page.add(
        ft.Column(
            [
                ft.Text("سبحان الله وبحمده", size=22, weight="w500", color="#374151"),
                ft.Container(height=30),
                circle_container,
                ft.Container(height=40),
                btn_tasbeeh,
                ft.Container(height=10),
                btn_reset,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
