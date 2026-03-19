"""CLI progress bar utility."""


def print_progress_bar(
    iteration: int,
    total: int,
    prefix: str = "",
    suffix: str = "",
    decimals: int = 1,
    length: int = 100,
    fill: str = "█",
    print_end: str = "\r",
) -> None:
    """Print a progress bar to the terminal.

    Args:
        iteration: Current iteration (0-based start is fine).
        total:     Total iterations.
        prefix:    Text before the bar.
        suffix:    Text after the bar.
        decimals:  Decimal places in the percentage.
        length:    Character width of the bar.
        fill:      Bar fill character.
        print_end: End character (default: carriage return).
    """
    if total <= 0:
        print(f'{prefix} |{"-" * length}| 100.0% {suffix}', flush=True)
        return
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end, flush=True)
    if iteration == total:
        print()