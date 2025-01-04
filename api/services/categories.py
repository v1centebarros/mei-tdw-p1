from transformers import pipeline


class CategoryService:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification",
                                   model="facebook/bart-large-mnli")

        self.labels = [
            "Computer Science",
            "Physics",
            "Biology and Medicine",
            "Engineering",
            "Mathematics",
            "Social Sciences",
            "Environmental Science",
            "Chemistry",
            "Earth Sciences",
            "Education",
            "Philosophy",
            "Linguistics",
            "Statistics",
            "Economics",
            "Information Science",
            "Neuroscience",
            "Agricultural Science",
            "Materials Science",
            "Astronomy",
            "Interdisciplinary Studies"
        ]

    def get_categories_for(self, markdown_text):
        markdown_text = markdown_text[:8192]
        result = self.classifier(markdown_text, self.labels, multi_class=True)

        categories = list()
        for i in range(len(result["labels"][:3])):
            if result["scores"][i] > 0.80:
                categories.append(result["labels"][i])

        return categories

    def get_all_categories(self):
        return self.labels
