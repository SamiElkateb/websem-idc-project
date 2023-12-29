import spotlight

# DB_SPOTLIGHT_URL = "https://api.dbpedia-spotlight.org/en/annotate"
DB_SPOTLIGHT_URL = "http://localhost:8080/rest/annotate"


def __get_annotations__(text: str, confidence, support):
    try:
        return spotlight.annotate(
            DB_SPOTLIGHT_URL, text, confidence=confidence, support=support
        )
    except Exception:
        return None


def get_food_item(text: str, confidence=0.2, support=20):
    result = __get_annotations__(text, confidence, support)
    if not result:
        result = __get_annotations__(text.capitalize(), confidence, support)
    if result:
        return sorted(result, key=lambda x: x.get('support'), reverse=True)
