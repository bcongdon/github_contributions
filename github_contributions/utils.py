COLOR_LEVELS = [
    '#ebedf0',
    '#9be9a8',
    '#40c463',
    '#30a14e',
    '#216e39'
]

CSS_COLOR_MAP = {
    "var(--color-calendar-graph-day-bg)": "#ebedf0",
    "var(--color-calendar-graph-day-L1-bg)": "#9be9a8",
    "var(--color-calendar-graph-day-L2-bg)": "#40c463",
    "var(--color-calendar-graph-day-L3-bg)": "#30a14e",
    "var(--color-calendar-graph-day-L4-bg)": "#216e39"
}


def level_for_fill(fill):
    hex_color = CSS_COLOR_MAP[fill]
    return COLOR_LEVELS.index(hex_color)
