class CategoriesSupplier(object):

    def __init__(self, categories):
        self._categories = categories

    def _matches(self, category, key):
        return category.lower().startswith(key.lower())

    def all(self):
        return self._categories

    def search(self, key):
        return [c for c in self._categories if self._matches(c, key)]
