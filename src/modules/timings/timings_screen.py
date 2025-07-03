from models.timings_model import Timings


def timings_screen(timings: list[Timings] | None) -> str:
    if not timings:
        return "No timings available."

    return "\n".join([f"{timing.number}: {timing.start}" for timing in timings])