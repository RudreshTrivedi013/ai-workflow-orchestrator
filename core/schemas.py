CALENDAR_VALIDATION_SCHEMA = {
    "is_calendar_request": "bool",
    "confidence": "float",
    "cleaned_text": "str"
}

CALENDAR_PARSE_SCHEMA = {
    "action": "str",
    "title": "str",
    "date": "str",
    "time": "str",
    "participants": "list"
}

BLOG_PLAN_SCHEMA = {
    "sections": "list",
    "word_count_per_section": "list",
    "style": "str"
}
