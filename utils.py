def snake_to_title(text: str) -> str:
    words = text.split("_")
    PascalCase = " ".join(word.title() for word in words)
    return PascalCase