import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from markdown import markdown
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
from slugify import slugify


env = Environment(
    loader=PackageLoader("blogpy"),
    autoescape=select_autoescape()
)


def tags_from_string(string: str) -> list[str]:
	splitted = string.split(",")
	tags = []
	for tag in splitted:
		if tag.startswith("#"):
			tag = tag[1:]
		tag = slugify(tag)
		if tag == "":
			continue
		tags.append(tag)
	return tags


@dataclass
class Tag:
	name: str


class Article:
	def __init__(self, author="Unknown", publish_date=datetime.now(), tags=str, content=""):
		self.author = author
		self.publish_date = publish_date
		self.tags = tags_from_string(tags)
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

	def infos(self):
		return {
			"author": self.author,
			"publish_date": self.publish_date,
			"tags": self.tags,
			"content": self.to_html()
		}

@dataclass
class Site:
	title: str
	description: str
	year: str

def copy_static(src: Path, dst: Path) -> None:
	if dst.exists():
		shutil.rmtree(dst)
	shutil.copytree(src, dst)

def get_article(content_path):
	var = {}
	with open(content_path, "r") as f:
		while (line := f.readline()) != "\n":
			name_var, val_var = line.split("=")
			var[name_var.strip()] = val_var.strip()
		article = Article(author=var["author"], publish_date=var["publish_date"], tags=var.get("tags", ""), content=''.join(f.readlines()))


	return article

def write_html(build_path, html):
	os.makedirs(build_path.parent, exist_ok=True)
	with open(build_path, "w+") as f:
		f.write(html)


def build(content_path, build_path):
	content_path = Path(content_path)
	build_path = Path(build_path)
	site = Site(title="Blog de Melcore", description="Le blog de la connaissance et du avoir peu commun", year=datetime.now().year)

	copy_static(Path("blogpy/templates/static"), build_path / "static")

	for child in content_path.iterdir():
		filename = child.stem
		article = get_article(child)
		article_template = env.get_template("article.html")
		article.content = article_template.render(article=article.infos(), site=site)
		write_html(build_path /(filename + ".html"), article.content)

