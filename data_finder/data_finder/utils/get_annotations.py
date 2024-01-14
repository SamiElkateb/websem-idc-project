import spotlight

from utils.is_food import check_is_food

# DB_SPOTLIGHT_URL = "https://api.dbpedia-spotlight.org/en/annotate"
DB_SPOTLIGHT_URL = "http://localhost:8080/rest/annotate"


def __get_annotations__(text: str, confidence, support):
    try:
        return spotlight.annotate(
            DB_SPOTLIGHT_URL, text, confidence=confidence, support=support
        )
    except Exception:
        return None


def process_result(result):
    list_result = result
    if not isinstance(result, list):
        list_result = [result]

    sorted_result = sorted(list_result, key=lambda x: x.get("support"), reverse=True)
    is_food = check_is_food(sorted_result[0]["URI"])
    if is_food:
        return sorted_result[0]
    print(sorted_result[0]["URI"], "is not food")


def get_food_item(texts, confidence=0.2, support=20):
    for keyword in texts:
        result = __get_annotations__(keyword[0], confidence, support)
        if result:
            result = process_result(result)

        if not result:
            result = __get_annotations__(keyword[0].capitalize(), confidence, support)

        if result:
            result = process_result(result)
        if result:
            return result
