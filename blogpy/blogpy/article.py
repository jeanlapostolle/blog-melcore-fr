from datetime import datetime

from markdown import markdown

from blogpy.blogpy.tag import tags_from_string


class Article:
    articles = []

    def __init__(
        self,
        author="Unknown",
        title: str = "",
        publish_date=datetime.now(),
        tags: str = "",
        content="",
    ):
        self.build_from_var(author, title, publish_date, tags, content)
        Article.articles.append(self)

    def build_from_var(
        self,
        author="Unknown",
        title: str = "",
        publish_date=datetime.now(),
        tags: str = "",
        content="",
    ):
        self.author = author
        self.publish_date = publish_date
        self.tags = tags_from_string(tags)
        self.content = content
        self.content = self.to_html()
        self.title = title

    def to_html(self):
        return markdown(
            self.content,
            extensions=["fenced_code", "codehilite"],
            extension_configs={"codehilite": {"linenums": False, "guess_lang": False}},
        )
        # TODO: Pygmentize command and add style.
        # pygmentize -S default -f html -a .codehilite > build/pygments.css
        # <link rel="stylesheet" href="pygments.css">

    def infos(self):
        return {
            "title": self.title,
            "author": self.author,
            "publish_date": self.publish_date,
            "tags": self.tags,
            "content": self.to_html(),
        }

    @classmethod
    def get_articles(cls):
        return Article.articles

    def from_markdown(self, content_path):
        var = {}
        with open(content_path, "r") as f:
            while (line := f.readline()) != "\n":
                name_var, val_var = line.split("=")
                var[name_var.strip()] = val_var.strip()

            self.build_from_var(**var, content="".join(f.readlines()))
        return self
