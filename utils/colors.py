def get_node_color(corr):
    """
    Returns the color of the node of the graph based on the correlation value.
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    blue = hex_to_rgb("#0000FF")
    white = hex_to_rgb("#FFFFFF")
    red = hex_to_rgb("#FF0000")
    if corr < 0:
        norm = (corr + 1) 
        rgb = tuple(int(blue[i] + norm * (white[i] - blue[i])) for i in range(3))
    else:
        norm = corr 
        rgb = tuple(int(white[i] + norm * (red[i] - white[i])) for i in range(3))
    return rgb_to_hex(rgb)
