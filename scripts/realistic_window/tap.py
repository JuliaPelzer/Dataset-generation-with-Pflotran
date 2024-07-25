def estimate_plume_shapeparams_tap(v_tech: float, delta_t: int, v_d: float, b: float) -> tuple[float]:
    # return length and width of heat plume in meters, acc. to formula from Fabian's poster (thermal anomaly size)
    length = 0.54 * v_tech**1.5 * delta_t**1.96 * (v_d * b)**(-1.5)
    width = 1.16 * v_tech * delta_t**0.76 * (v_d * b)**(-1)
    return length, width