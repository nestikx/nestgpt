import flet as ft
import asyncio
import os

import gpt, pages, ns


class Message(ft.Row):
    def __init__(self, page: ft.Page, message: str, role: str):
        super().__init__()

        roles = [
            # position
            {
                "me": ft.MainAxisAlignment.END,
                "bot": ft.MainAxisAlignment.START,
                "system": ft.MainAxisAlignment.CENTER
            },
            # color
            {
                "me": [ft.Colors.PRIMARY_CONTAINER, ft.Colors.ON_PRIMARY_CONTAINER],
                "bot": [ft.Colors.SURFACE, ft.Colors.ON_SURFACE],
                "system": [ft.Colors.INVERSE_SURFACE, ft.Colors.ON_INVERSE_SURFACE]
            },
            # size
            {
                "me": 16,
                "bot": 16,
                "system": 14
            },
            # align
            {
                "me": ft.MainAxisAlignment.START,
                "bot": ft.MainAxisAlignment.START,
                "system": ft.MainAxisAlignment.CENTER
            }
        ]

        self.controls = [
            ft.Container(
                ft.Markdown(
                    value = message,
                    selectable = True,
                    extension_set = ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link = lambda e: page.launch_url(e.data),
                    md_style_sheet = ft.MarkdownStyleSheet(
                        p_text_style = ft.TextStyle(
                            size = roles[2][role],
                            color = roles[1][role][1],
                            bgcolor = roles[1][role][0]
                        ),
                        text_alignment = roles[3][role]
                    ),
                    code_theme = ft.MarkdownCodeTheme.ANDROID_STUDIO,
                    code_style_sheet = ft.MarkdownStyleSheet(
                        code_text_style = ft.TextStyle(font_family = "Cascadia Code")
                    )
                ),
                padding = 10,
                border_radius = 20,
                bgcolor = roles[1][role][0],
                scale = 1,
                animate_scale = ft.Animation(duration = 200, curve = ft.AnimationCurve.EASE),
                expand = True,
                expand_loose = True
            )
        ]
        self.alignment = roles[0][role]


async def main(page: ft.Page):
    await pages.load(page, gpt.init)
    page.controls.clear()

    page.title = "Nuxt GPT"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.SURFACE
    page.fonts = {
        "Nunito-Bold": "fonts/Nunito-Bold.ttf",
        "PollyRounded-Bold": "fonts/PollyRounded-Bold.ttf"
    }
    page.theme = ft.Theme(font_family = "Nunito-Bold")
    
    messages = []

    async def send_msg(message: str, role: str):
        chat.content.controls.append(Message(page, message, role))
        chat.content.scroll_to(offset = -1, duration = 200, curve = ft.AnimationCurve.EASE)
        chat.content.controls[-1].controls[0].scale = 0
        page.update()

        await asyncio.sleep(0.1)
                
        chat.content.controls[-1].controls[0].scale = 1
        page.update()
    
    async def ask(message: str):
        answer = await asyncio.to_thread(gpt.question, message, messages)
        await send_msg(answer, "bot")

    async def click_send(e):
        send_button.content.scale = 1
        page.update()

        await asyncio.sleep(0.1)

        send_button.content.scale = 1.4
        page.update()

        if message_field.value.strip() != "":
            if message_field.value == "err.null":
                page.controls.clear()
                pages.err(page)
            else:
                await send_msg(message_field.value, "me")

                message = message_field.value
                message_field.value = ""
                page.update()
                await ask(message)

    def switch_mode(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            switch_mode_button.icon = ft.Icons.NIGHTLIGHT_ROUNDED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch_mode_button.icon = ft.Icons.WB_SUNNY_ROUNDED
        
        page.update()
    
    title_text = ft.Text(
        value = "Nuxt GPT",
        font_family = "PollyRounded-Bold",
        size = 32
    )

    creator_name = ft.Text(
        value = "by nestik",
        font_family = "PollyRounded-Bold",
        size = 16
    )
    
    switch_mode_button = ft.IconButton(
        icon = ft.Icons.WB_SUNNY_ROUNDED,
        icon_size = 30,
        icon_color = ft.Colors.ON_PRIMARY_CONTAINER,
        animate_scale = ft.Animation(duration = 200, curve = ft.AnimationCurve.EASE),
        on_click = switch_mode
    )

    send_button = ft.Container(
        ft.Image(
            src = "image/send_duotone.svg",
            scale = 1.4,
            color = ft.Colors.ON_SURFACE,
            animate_scale = ft.Animation(duration = 200, curve = ft.AnimationCurve.EASE)
        ),
        ink = True,
        padding = 12,
        border_radius = 40,
        bgcolor = ft.Colors.SURFACE,
        on_click = click_send
    )

    message_field = ft.TextField(
        hint_text = "Enter message",
        border_color = "transparent",
        bgcolor = ft.Colors.SURFACE,
        border_radius = 40,
        multiline = True,
        expand = True
    )

    panel = ft.Container(
        ft.Row(
            [
                title_text,
                ft.Row(
                    [
                        creator_name,
                        switch_mode_button,
                    ],
                    alignment = ft.MainAxisAlignment.END
                )
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        margin = 10
    )

    chat = ft.Container(
        ft.Column(
            [
                Message(page, "active model gpt-4o", "system")
            ],
            scroll = ft.ScrollMode.AUTO
        ),
        expand = True
    )

    messbox = ft.Container(
        ft.Row(
            [
                message_field,
                send_button
            ],
            width = 400
        ),
        margin = 20,
        padding = 20,
        border_radius = 50,
        bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
    )

    page.add(
        ft.Column(
            [
                panel,
                chat,
                messbox
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True
        )
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2496))
    ft.app(target = main, view = ft.WEB_BROWSER, port = port)