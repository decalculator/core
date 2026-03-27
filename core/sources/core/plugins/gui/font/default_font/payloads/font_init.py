from core.plugins.gui.font.default_font.default_font import Default_font

async def bridge(gui):
    uuid = dpg.generate_uuid()
    default_font = Default_font(uuid, gui)
    default_font.register()
    dpg.bind_font(uuid)