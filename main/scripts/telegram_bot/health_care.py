def calculate_water(weight: int) -> tuple[float, float]:
    min_water: int = 20
    max_water: int = 40
    result_min = round(min_water * weight / 1000, 2)
    result_max = round(max_water * weight / 1000, 2)
    return result_min, result_max

