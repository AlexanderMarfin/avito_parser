# Словарь с клавиатурами для генерации
KEYBOARDS: dict[str, [str]] = {
    "transmission": ("automatic", "variable", "robotic", "manual"),
    "gear": ("rear-wheel", "front-wheel", "four-wheel"),
    "engine": ("petrol", "diesel", "electric", "gas", "hybrid"),
    "start_parse": ("reset_data", "start_parsing"),
    "statistics": ("info", "plot", "menu"),
    "start_menu": ("unloading", "auto_finder"),
    "unloading_menu": ("auto_parse", "flat_parse", "back"),
    "error_menu": ("retry", "menu"),
}
