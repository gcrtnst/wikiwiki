import argparse
import bs4
import requests
import urllib.parse


def main() -> None:
    argp = argparse.ArgumentParser()
    subp = argp.add_subparsers(dest="cmd", required=True)

    getp = subp.add_parser("get")
    getp.add_argument("wiki")
    getp.add_argument("page")

    args = argp.parse_args()
    if args.cmd == "get":
        get(args.wiki, args.page)
    else:
        raise RuntimeError


def get(wiki: str, page: str) -> None:
    sess = requests.Session()
    try:
        del sess.headers["User-Agent"]
    except KeyError:
        pass

    url = (
        "https://wikiwiki.jp/"
        + urllib.parse.quote(wiki, safe="", encoding="utf-8", errors="strict")
        + "/?cmd=edit&page="
        + urllib.parse.quote_plus(page, safe="", encoding="utf-8", errors="strict")
    )
    resp = sess.get(url)
    resp.raise_for_status()

    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    tag = soup.select_one("#original-data-temp")
    text = tag.attrs["value"] if tag is not None else ""
    print(text, end="")


if __name__ == "__main__":
    main()
