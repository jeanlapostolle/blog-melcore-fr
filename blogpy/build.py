import os
import shutil
from dataclasses import dataclass
from pathlib import Path


from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape

from blogpy.blogpy.article import Article
from blogpy.blogpy.site import Site
from blogpy.blogpy.utils import copy_static, get_article, write_html

env = Environment(
    loader=PackageLoader("blogpy"),
    autoescape=select_autoescape()
)


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

