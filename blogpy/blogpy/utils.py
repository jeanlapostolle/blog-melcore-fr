import os
import shutil
from pathlib import Path

from blogpy.blogpy.article import Article


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
		article = Article(author=var["author"], title=var["title"],publish_date=var["publish_date"], tags=var.get("tags", ""), content=''.join(f.readlines()))


	return article

def write_html(build_path, html):
	os.makedirs(build_path.parent, exist_ok=True)
	with open(build_path, "w+") as f:
		f.write(html)
