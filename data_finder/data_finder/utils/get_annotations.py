import spotlight

DB_SPOTLIGHT_URL = "https://api.dbpedia-spotlight.org/en/annotate"


def get_annotations(texts: list | str, confidence=0.6, support=20):
    if type(texts) == list:
        data = []
        for text in texts:
            annotations = spotlight.annotate(
                DB_SPOTLIGHT_URL, text, confidence=confidence, support=support
            )
            data.append(annotations)
        return data
    else:
        return spotlight.annotate(DB_SPOTLIGHT_URL, texts, confidence=0.1, support=10)
