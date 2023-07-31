import os


def beep(case: str = "end"):
    duration = 0.05  # seconds
    freq = 440  # Hz
    os.system(f"play -nq -t alsa synth {duration} sine {freq}")
    if case == "end":
        freq = 640  # Hz
        os.system(f"play -nq -t alsa synth {duration} sine {freq}")
