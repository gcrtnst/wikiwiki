import argparse
import bs4
import copy
import requests
import urllib.parse


def main() -> None:
    argp = argparse.ArgumentParser()
    subp = argp.add_subparsers(dest="cmd", required=True)

    getp = subp.add_parser("gethtml")
    getp.add_argument("wiki")
    getp.add_argument("page")
    getp.add_argument("--pretty", action="store_true")

    args = argp.parse_args()
    if args.cmd == "gethtml":
        gethtml(args.wiki, args.page, pretty=args.pretty)
    else:
        raise RuntimeError


def gethtml(wiki: str, page: str, *, pretty: bool = False) -> None:
    sess = requests.Session()
    try:
        del sess.headers["User-Agent"]
    except KeyError:
        pass

    url = (
        "https://wikiwiki.jp/"
        + urllib.parse.quote(wiki, safe="", encoding="utf-8", errors="strict")
        + "/"
        + urllib.parse.quote_plus(page, safe="/", encoding="utf-8", errors="strict")
    )
    resp = sess.get(url)
    resp.raise_for_status()

    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    elem = soup.select_one("#content")
    text = ""
    if elem is not None:
        elem = copy.copy(elem)
        for chld in elem.select("div.caption-flybox") + elem.select("script"):
            chld.decompose()

        text = elem.prettify() if pretty else str(elem)
    print(text, end="")


if __name__ == "__main__":
    main()
