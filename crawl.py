import urllib.parse

def normalize_url(url: str):
    split = urllib.parse.urlsplit(url)
    string = f"{split.netloc}{split.path}"
    return string.removesuffix("/")