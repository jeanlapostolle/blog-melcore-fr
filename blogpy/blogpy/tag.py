from dataclasses import dataclass

from slugify import slugify


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
