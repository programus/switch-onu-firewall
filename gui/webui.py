import asyncio
from typing import Optional
from nicegui import (
    ui,
    app,
)
from fastapi.responses import RedirectResponse

from gui.middleware import AuthMiddleware
from webclient import fw_switcher
from config import (
    webui,
    app as app_settings,
)


current_level = fw_switcher.FirewallLevel.loading

app.add_middleware(AuthMiddleware)

@ui.refreshable
def update_firewall_level():
    global current_level
    if current_level is None:
        ui.label("Failed to retrieve current firewall level").classes("text-lg mb-4").style("color: red;")
    elif current_level == fw_switcher.FirewallLevel.loading:
        with ui.row():
            ui.label("Current firewall level:").classes("text-lg mb-4")
            ui.skeleton('text').classes("text-lg mb-4 w-16")
        ui.label("Set Firewall Level:").classes("text-lg mt-4 mb-2")
        ui.skeleton('rect').classes("h-10 w-64")
    else:
        ui.label(f"Current firewall level: {current_level.name}").classes("text-lg mb-4")
        ui.label("Set Firewall Level:").classes("text-lg mt-4 mb-2")
        levels_radio = ui.radio({l.value: l.name for l in fw_switcher.FirewallLevel if l.value >= 0}, value=current_level.value)

        ui.button("Set Level", on_click=lambda: set_firewall_level(fw_switcher.FirewallLevel(levels_radio.value))).classes("mt-4")



async def load_firewall_level():
    global current_level
    current_level = await asyncio.to_thread(fw_switcher.get_current_firewall_level)
    update_firewall_level.refresh()


async def set_firewall_level(level: fw_switcher.FirewallLevel):
    global current_level
    current_level = fw_switcher.FirewallLevel.loading
    update_firewall_level.refresh()

    new_level = await asyncio.to_thread(lambda: fw_switcher.set_firewall_level(level))
    if new_level:
        ui.notify(f"Firewall level set to: {new_level.name}")
        current_level = new_level
    else:
        current_level = None
        ui.notify("Failed to set firewall level", color="negative")
    update_firewall_level.refresh()


@ui.page('/')
def main_page():
    def logout():
        app.storage.user.clear()
        ui.navigate.to('/login')
    global current_level
    current_level = fw_switcher.FirewallLevel.loading
    with ui.header().classes("justify-between items-center w-full"):
        ui.markdown(f"**Switch ONU Firewall Level** - _{app.storage.user.get('username')}_")
        ui.button("Logout", color='negative', on_click=logout).classes("").props('flat')
    with ui.card().classes("w-full"):
        update_firewall_level()
    asyncio.create_task(load_firewall_level())


@ui.page('/login')
def login_page(redirect_to: str = '/') -> Optional[RedirectResponse]:
    def authenticate():
        if (username_input.value, password_input.value) == (app_settings.username, app_settings.password):
            app.storage.user.update({
                'authenticated': True,
                'username': username_input.value,
            })
            ui.notify("Login successful", color="positive")
            ui.navigate.to(redirect_to)
        else:
            ui.notify("Invalid credentials", color="negative")

    if app.storage.user.get('authenticated'):
        return RedirectResponse(url='/')

    with ui.card().classes('absolute-center'):
        username_input = ui.input('Username').on('keydown.enter', authenticate)
        password_input = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', authenticate)
        ui.button('Login', on_click=authenticate)
    return None


def start_webui():
    ui.run(title="Switch ONU Firewall", host=webui.host, port=webui.port, storage_secret=app_settings.storage_secret)