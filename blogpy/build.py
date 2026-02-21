import os
from dataclasses import dataclass
from pathlib import Path
from markdown import markdown
from datetime import datetime


class Article:
	def __init__(self, author="Unknown", publish_date=datetime.now(), tags=[], content=""):
		self.author = author
		self.publish_date = publish_date
		self.tags = tags
		self.content = content

	def to_html(self):
		return markdown(self.content, extensions=[
		        "fenced_code",
		        "codehilite"
		    ],
		    extension_configs={
		        "codehilite": {
		            "linenums": False,
		            "guess_lang": False
		        }
		    })
			# TODO: Pygmentize command and add style.
			# pygmentize -S default -f html -a .codehilite > build/pygments.css
			# <link rel="stylesheet" href="pygments.css">

def get_article(content_path):
	var = {}
	with open(content_path, "r") as f:
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

def write_html(build_path, html):
	os.makedirs(build_path.parent, exist_ok=True)
	with open(build_path, "w+") as f:
		f.write(html)


def build(content_path, build_path):
	content_path = Path(content_path)
	build_path = Path(build_path)

	for child in content_path.iterdir():
		filename = child.stem
		article = get_article(child)
		write_html(build_path /(filename + ".html"), article.to_html())

