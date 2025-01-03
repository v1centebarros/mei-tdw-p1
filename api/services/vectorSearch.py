from sentence_transformers import SentenceTransformer


class VectorSearchService:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def index(self, markdown_text: str):
        text = markdown_text.splitlines()
        text = [t for t in text if t]
        embeddings = self.model.encode(text)

        result = []
        counter = 0
        for i, sent in enumerate(text):
            result.append({
                "embedding": embeddings[i],
                "segment_id": counter
            })
            counter += len(sent)

        return result
