
def day_to_num(day: str):
    match day:
        case "ПОНЕДЕЛЬНИК":
            return 1
        case "ВТОРНИК":
            return 2
        case "СРЕДА":
            return 3
        case "ЧЕТВЕРГ":
            return 4
        case "ПЯТНИЦА":
            return 5
        case "СУББОТА":
            return 6
        case "ВОСКРЕСЕНЬЕ":
            return 7
        case _:
            return 0