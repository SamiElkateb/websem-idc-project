from pke.unsupervised import MultipartiteRank

extractor = MultipartiteRank()

with open("datasets/WKC/docsutf8/43971.txt") as f:
    doc = f.read()
extractor.load_document(doc)
