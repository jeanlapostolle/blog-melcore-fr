from pathlib import Path
from markdown import markdown


def get_mardown(content_url):
	var = {}
	with open(content_url, "r") as f:
		while (line := f.readline()) != "\n":
			name_var, val_var = line.strip().split("=")
			var[name_var] = val_var
		md = ''.join(f.readlines())
	return var, md


class Builder:
	def __init__(self, content_url:Path):
		self.content_url = content_url

	def build(self):
		var, md = get_mardown(self.content_url)
		html = markdown(md)
		with open(self.content_url+".html", "w") as f:
			print(var["author"], var["publish_date"])
			f.write(html)





