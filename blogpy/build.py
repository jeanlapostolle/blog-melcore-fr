from pathlib import Path
from markdown import markdown
from datetime import datetime

@dataclasses
class Article:
	author = "<NAME>"
	publish_date = datetime.today()
	tags = []
	content = ""

	def to_html(self):
		return markdown(self.content)


def get_markdown(content_url):
	var = {}
	with open(content_url, "r") as f:
		while (line := f.readline()) != "\n":
			name_var, val_var = line.split("=")
			var[name_var.split()] = val_var.split()
		article = Article(author=var["author"], publish_date=var["publish_date"])
		article.content = ''.join(f.readlines())

	for name, value in var.items():
		if name in article.__dict__:
			article.__dict__[name] = value
		else:
			raise NameError(f"Variable {name} is not a valid variable name")

	return article


class Builder:
	def __init__(self, content_url:Path):
		self.content_url = content_url

	def build(self):
		article= get_markdown(self.content_url)
		with open(self.content_url+".html", "w") as f:
			print(article["author"], article["publish_date"])
			f.write(article.to_html())
