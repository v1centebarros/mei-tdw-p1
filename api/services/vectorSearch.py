from sentence_transformers import SentenceTransformer

from crud.vectorSearch import search_by_vector
from sqlalchemy.orm import Session



class VectorSearchService:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def index(self, markdown_text: str):
        text = markdown_text.splitlines()
        filtered_text = [t for t in text if t]
        embeddings = self.model.encode(filtered_text)

        result = []
        counter = 0
        emb_ix = 0
        for i, sent in enumerate(text):
            if len(sent) == 0:
                counter += 1
            else:
                result.append({
                    "embedding": embeddings[emb_ix],
                    "start_position": counter,
                    "end_position": counter + len(sent) + 1
                })
                counter += len(sent) + 1
                emb_ix += 1

        return result

    def get_query_embedding(self, query: str):
        return self.model.encode(query).tolist()

    # def search_by_vector(self, db: Session, query: str):
    #     query_vec = self.get_query_embedding(query)
    #     results = search_by_vector(db, query_vec)
    #
    #     final_results = list()
    #     files = [res[1] for res in results]
    #     unique_files = set(files)
    #     for file in unique_files:
    #         content = file.content
    #         rank = None
    #         count = 0
    #         for i, sres in enumerate(sorted(results, key=lambda x: x[0].start_position)):
    #             if sres[1].id == file.id:
    #                 res = sres[0]
    #                 off = count * len("<mark></mark>")
    #                 content = content[:off + res.start_position] + "<mark>" + content[off + res.start_position:off + res.end_position] + "</mark>" + content[off + res.end_position:]
    #                 if rank is None:
    #                     rank = sres[2]
    #                 else:
    #                     rank += sres[2]
    #                 count += 1
    #
    #         final_results.append({
    #             "file_id": file.id,
    #             "filename": file.filename,
    #             "content_type": file.content_type,
    #             "content_preview": content,
    #             "categories": file.categories,
    #             "rank": 1 - rank / count
    #         })
    #
    #     return sorted(final_results, key=lambda x: x["rank"], reverse=True)

    def search_by_vector(self, db: Session, query: str, context_range: int = 400):
        query_vec = self.get_query_embedding(query)
        results = search_by_vector(db, query_vec)

        final_results = []
        files = [res[1] for res in results]
        unique_files = set(files)

        for file in unique_files:
            content = file.content
            rank = None
            count = 0
            marked_sentences = []  # List to store sentences with marked phrases

            # Sort results by start_position for consistent processing
            for i, sres in enumerate(sorted(results, key=lambda x: x[0].start_position)):
                if sres[1].id == file.id:
                    res = sres[0]
                    start_pos = res.start_position
                    end_pos = res.end_position

                    # Extract context around the marked phrase
                    context_start = max(0, content.rfind(' ', 0, start_pos - context_range) + 1 if start_pos > context_range else 0)
                    context_end = min(len(content),
                                      content.find(' ', end_pos + context_range) if content.find(' ', end_pos + context_range) != -1 else len(
                                          content))

                    # Mark the phrase and append the surrounding context
                    marked_phrase = (content[context_start:start_pos] + "<mark>" +
                                     content[start_pos:end_pos] + "</mark>" +
                                     content[end_pos:context_end])
                    marked_sentences.append(marked_phrase)

                    if rank is None:
                        rank = sres[2]
                    else:
                        rank += sres[2]
                    count += 1

            # Prepare the final result for this file
            final_results.append({
                "file_id": file.id,
                "filename": file.filename,
                "content_type": file.content_type,
                "content_preview": marked_sentences,  # List of marked sentences
                "categories": file.categories,
                "rank": 1 - rank / count
            })

        return sorted(final_results, key=lambda x: x["rank"], reverse=True)
