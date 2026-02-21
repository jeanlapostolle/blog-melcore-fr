from dataclasses import dataclass
from pathlib import Path
from markdown import markdown
from datetime import datetime


class Article:
	def __init__(self, author="Unkown", publish_date=datetime.now(), tags=[], content=""):
		self.author = author
		self.publish_date = publish_date
		self.tags = tags
		self.content = content

	def to_html(self):
		return markdown(self.content)


def get_markdown(content_url):
	var = {}
	with open(content_url, "r") as f:
		while (line := f.readline()) != "\n":
			name_var, val_var = line.split("=")
			var[name_var.strip()] = val_var.strip()
		article = Article()
		article.content = ''.join(f.readlines())

	for name, value in var.items():
		if name in article.__dict__:
			article.__dict__[name] = value
		else:
			raise NameError(f"Variable {name} is not a valid variable name")

	return article



def build(content_url):
	article= get_markdown(content_url)
	with open(content_url+".html", "w") as f:
		print(article.author, article.publish_date)
		f.write(article.to_html())
