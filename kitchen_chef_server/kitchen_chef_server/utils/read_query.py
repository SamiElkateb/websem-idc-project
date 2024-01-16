def read_query(path):
    data = ""
    with open(path) as f:
        data = f.read()
    return data
