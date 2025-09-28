from nicegui import (
    ui,
    app,
)
from webclient import fw_switcher
from env import (
    listen_host,
    listen_port,
)
import asyncio


current_level = fw_switcher.FirewallLevel.loading


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
    global current_level
    current_level = fw_switcher.FirewallLevel.loading
    ui.label("Switch ONU Firewall Level").classes("text-2xl font-bold mb-4")
    update_firewall_level()
    asyncio.create_task(load_firewall_level())


def start_webui():
    ui.run(title="Switch ONU Firewall", host=listen_host, port=listen_port)