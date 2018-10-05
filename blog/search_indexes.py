from haystack import indexes
from .models import Article

class ArticleIndex(indexes.SearchIndex,indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)

	def get_model(self):
		return Article

	def index_qureyset(self,using=None):
		return self.get_model().objects.all()