def get_rgb_int(widget):
    rgb = widget.winfo_rgb(widget["bg"])  # 16-bit RGB Werte
    r, g, b = (rgb[0] // 256, rgb[1] // 256, rgb[2] // 256)  # 8-bit
    return (r << 16) | (g << 8) | b  # integer

def int_to_hex_str(farbwert):
    return f"#{farbwert:06x}"
