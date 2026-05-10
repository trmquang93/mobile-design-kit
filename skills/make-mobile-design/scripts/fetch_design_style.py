#!/usr/bin/env python3
"""Fetch brand design styles from VoltAgent/awesome-design-md.

Subcommands:
  list           Print JSON array of available brand slugs.
  fetch <brand>  Download that brand's DESIGN.md and print to stdout (or --out).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

INDEX_URL = "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md"
RAW_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{brand}/DESIGN.md"
CACHE_PATH = "/tmp/awesome-design-md-index.json"


def http_get(url: str, accept: str = "application/json") -> bytes:
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "make-mobile-design-skill"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def cmd_list(args: argparse.Namespace) -> int:
    if not args.refresh and os.path.exists(CACHE_PATH):
        with open(CACHE_PATH) as f:
            print(f.read())
        return 0
    try:
        data = json.loads(http_get(INDEX_URL))
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"error: failed to fetch brand index: {e}", file=sys.stderr)
        return 2
    brands = sorted(item["name"] for item in data if item.get("type") == "dir")
    out = json.dumps(brands, indent=2)
    try:
        with open(CACHE_PATH, "w") as f:
            f.write(out)
    except OSError:
        pass
    print(out)
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    url = RAW_URL.format(brand=args.brand)
    try:
        body = http_get(url, accept="text/plain").decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"error: brand '{args.brand}' not found in awesome-design-md", file=sys.stderr)
            return 3
        print(f"error: HTTP {e.code} fetching {url}", file=sys.stderr)
        return 2
    except urllib.error.URLError as e:
        print(f"error: network failure: {e}", file=sys.stderr)
        return 2
    if args.out:
        with open(args.out, "w") as f:
            f.write(body)
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(body)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("list", help="list available brand slugs")
    pl.add_argument("--refresh", action="store_true", help="bypass local cache")
    pl.set_defaults(func=cmd_list)
    pf = sub.add_parser("fetch", help="fetch a brand's DESIGN.md")
    pf.add_argument("brand", help="brand slug (e.g. apple, stripe, linear.app)")
    pf.add_argument("--out", help="write to file instead of stdout")
    pf.set_defaults(func=cmd_fetch)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
