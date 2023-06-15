def format_too_long_str(text: str, _max: int) -> str:
    return text if len(text) <= _max else text[:(_max - 3)] + '...'