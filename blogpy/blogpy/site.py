from dataclasses import dataclass

from markdown import markdown


@dataclass
class Site:
    title: str = ""
    description: str = ""
    presentation: str = ""
    year: str = ""

    def to_html(self):
        return markdown(
            self.presentation,
            extensions=["fenced_code", "codehilite"],
            extension_configs={"codehilite": {"linenums": False, "guess_lang": False}},
        )

    def build_from_var(
        self,
        title: str,
        description: str,
        presentation: str,
        year: str,
    ):
        self.title = title
        self.description = description
        self.presentation = presentation
        self.presentation = self.to_html()
        self.year = year

    def from_markdown(self, content_path):
        var = {}
        with open(content_path, "r") as f:
            while (line := f.readline()) != "\n":
                name_var, val_var = line.split("=")
                var[name_var.strip()] = val_var.strip()

            self.build_from_var(**var, presentation="".join(f.readlines()))
        return self
