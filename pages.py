import flet as ft
import asyncio


error_text = """
    A problem has been detected on the website.
    Website closed to prevent damage.

    Unknown_Problem_Error.null
    STOP: 0x00e0null
"""

def err(page: ft.Page):
    print("[pages module]: 0x00e0null")
    page.title = "null"
    page.bgcolor = ft.Colors.BLUE_ACCENT_700
    page.fonts = {"PollyRounded-Bold": "fonts/PollyRounded-Bold.ttf"}
    page.theme = ft.Theme(font_family = "PollyRounded-Bold")

    page.add(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        value = " :(",
                        size = 160,
                        color = "white"
                    ),
                    ft.Text(
                        value = error_text,
                        size = 24,
                        color = "white"
                    )
                ],
                spacing = 80,
                alignment = ft.MainAxisAlignment.CENTER
            ),
            margin = 20
        )
    )

async def load(page: ft.Page, init_func):
    page.title = "load"
    page.bgcolor = ft.Colors.BLACK
    page.fonts = {"PollyRounded-Bold": "fonts/PollyRounded-Bold.ttf"}
    page.theme = ft.Theme(font_family = "PollyRounded-Bold")

    progres_ring = ft.ProgressRing(
           scale = 1.2,
           color = "white",
           stroke_width = 5,
           stroke_cap = ft.StrokeCap.ROUND,
           animate_opacity = ft.Animation(duration = 2000, curve = ft.AnimationCurve.EASE)
    )

    text = ft.Text(
        value = "gpt init",
        size = 20,
        color = "white",
        text_align = ft.TextAlign.CENTER,
        animate_opacity = ft.Animation(duration = 2000, curve = ft.AnimationCurve.EASE)
    )

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        progres_ring,
                        text
                    ],
                    spacing = 20,
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    expand = True
                )
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            expand = True
        )
    )

    async def anim_run():
        progres_ring.opacity = 0
        text.opacity = 0
        page.update()

        await asyncio.sleep(0.1)

        progres_ring.opacity = 1
        text.opacity = 1
        page.update()
    
    async def anim_close():
        progres_ring.opacity = 0
        text.opacity = 0
        page.update()
        await asyncio.sleep(2)
    
    await anim_run()
    await asyncio.to_thread(init_func)
    await anim_close()