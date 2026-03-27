from core.plugins.gui.themes.white_theme.white_theme import WhiteTheme

async def bridge(gui):
    uuid = dpg.generate_uuid()
    white_theme = WhiteTheme(uuid, gui)
    white_theme.register()
    dpg.bind_theme(uuid)