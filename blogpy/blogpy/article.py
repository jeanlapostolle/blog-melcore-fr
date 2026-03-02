from datetime import datetime

from markdown import markdown

from blogpy.blogpy.tag import tags_from_string


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