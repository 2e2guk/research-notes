#!/usr/bin/env python3
"""Check rendered reading navigation without adding posts to the real site.

Default: copy the site into a TemporaryDirectory, add five fixture posts, run
the caller's ``bundle exec jekyll build``, and inspect the generated HTML.

After a separate production build, run:
    python3 scripts/check_reading_navigation.py --production-dir _site

Only the standard library is used. Bundler's environment is inherited; when
BUNDLE_PATH is set by the caller, an absolute path is recommended.
"""

from __future__ import annotations

import argparse
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


MARKER = "READING_NAVIGATION_FIXTURE_"
FIXTURE_ROUTE = "__reading-navigation-fixture__"
SERIES = "OpenVLA 읽기"
COPY_EXCLUDES = {
    ".git", ".bundle", ".jekyll-cache", ".jekyll-metadata", ".sass-cache",
    "__pycache__", "node_modules", "vendor", "preview", "lighthouse_results",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list[Node | str] = field(default_factory=list)

    def descendants(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.descendants()

    def text(self) -> str:
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)


class Document(HTMLParser):
    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {key: value or "" for key, value in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_document(path: Path) -> Node:
    require(path.is_file(), f"Generated HTML is missing: {path}")
    return Document(path.read_text(encoding="utf-8")).root


def one_section(root: Node, attribute: str, value: str) -> Node:
    found = [node for node in root.descendants()
             if node.tag == "section" and node.attrs.get(attribute) == value]
    require(len(found) == 1,
            f"Expected one section[{attribute}={value!r}], found {len(found)}")
    return found[0]


def fixture_id(href: str) -> str | None:
    path = unquote(urlsplit(href).path)
    match = re.search(r"/" + re.escape(FIXTURE_ROUTE) + r"/([a-e])(?:/|$)", path)
    return match.group(1).upper() if match else None


def fixture_links(root: Node) -> set[str]:
    return {value for node in root.descendants() if node.tag == "a"
            if (value := fixture_id(node.attrs.get("href", ""))) is not None}


def reading_order(root: Node) -> list[str]:
    """Read ol.reading-posts > li > a[data-post-link] in DOM order."""
    result = []
    for listing in root.descendants():
        if listing.tag != "ol" or "reading-posts" not in listing.attrs.get("class", "").split():
            continue
        for item in listing.children:
            if not isinstance(item, Node) or item.tag != "li":
                continue
            for link in item.children:
                if isinstance(link, Node) and link.tag == "a" and "data-post-link" in link.attrs:
                    value = fixture_id(link.attrs.get("href", ""))
                    if value is not None:
                        result.append(value)
    return result


def baseurl_from_config(source: Path) -> str:
    for line in (source / "_config.yml").read_text(encoding="utf-8").splitlines():
        if re.match(r"^baseurl\s*:", line):
            parts = shlex.split(line.split(":", 1)[1], comments=True)
            return (parts[0] if parts else "").rstrip("/")
    return ""


def target_file(output: Path, href: str, baseurl: str) -> Path:
    """Map a rendered absolute/site-relative archive URL to its output file."""
    path = unquote(urlsplit(href).path)
    require(path.startswith("/"), f"Expected an absolute archive path: {href!r}")
    if baseurl:
        require(path == baseurl or path.startswith(baseurl + "/"),
                f"Archive link lost the configured baseurl {baseurl!r}: {href!r}")
        path = path[len(baseurl):]
    target = output / path.lstrip("/")
    require(target.resolve().is_relative_to(output.resolve()), f"Unsafe archive path: {href!r}")
    return target if target.suffix else target / "index.html"


def find_tag_link(tags: Node, tag: str) -> Node:
    matches = []
    for node in tags.descendants():
        if node.tag != "a" or "data-tag-link" not in node.attrs:
            continue
        label = " ".join(node.text().split()).lstrip("#").strip()
        # Also accept a badge such as 'policy (3)' or 'policy3'.
        if (node.attrs.get("data-tag-link") == tag
                or re.fullmatch(re.escape(tag) + r"(?:\s*[\[(]?\d+[\])]?)?", label)):
            matches.append(node)
    require(len(matches) == 1, f"Expected one tag link for {tag!r}, found {len(matches)}")
    return matches[0]


def add_fixtures(source: Path) -> None:
    # A is newest and B oldest: neither descending date nor string sorting can
    # accidentally satisfy the required B(2), A(10), C(no order) sequence.
    fixtures = [
        ("A", "2001-01-05", "vla", SERIES, 10, ["policy", "행동 토큰"]),
        ("B", "2001-01-01", "vla", SERIES, 2, ["policy"]),
        ("C", "2001-01-03", "vla", SERIES, None, ["행동 토큰"]),
        ("D", "2001-01-02", "tactile", "새 촉각 시리즈", 1, ["촉각"]),
        ("E", "2001-01-04", None, None, None, ["policy", "촉각"]),
    ]
    posts = source / "_posts"
    posts.mkdir(exist_ok=True)
    for key, date, topic, series, order, tags in fixtures:
        lines = ["---", "layout: post", f'title: "{MARKER}{key}"',
                 f"date: {date} 12:00:00 +0000",
                 f"permalink: /{FIXTURE_ROUTE}/{key.lower()}/",
                 "related_posts: false", "tags:"]
        lines.extend(f'  - "{tag}"' for tag in tags)
        if topic is not None:
            lines.append(f"topic: {topic}")
        if series is not None:
            lines.append(f'series: "{series}"')
        if order is not None:
            lines.append(f"series_order: {order}")
        lines.extend(["---", "", f"{MARKER}{key}: temporary navigation check only.", ""])
        (posts / f"{date}-{FIXTURE_ROUTE}-{key.lower()}.md").write_text(
            "\n".join(lines), encoding="utf-8")


def check_rendered_navigation(output: Path, baseurl: str) -> None:
    home = read_document(output / "index.html")
    vla = one_section(home, "data-topic", "vla")
    tactile = one_section(home, "data-topic", "tactile")
    other = one_section(home, "data-topic", "other")
    series = one_section(vla, "data-series", SERIES)
    require(reading_order(series) == ["B", "A", "C"],
            f"Series order must be B(2), A(10), C(missing), got {reading_order(series)}")
    require(fixture_links(vla) == {"A", "B", "C"}, "VLA topic fixture membership is incorrect")
    require(fixture_links(tactile) == {"D"}, "Tactile topic fixture membership is incorrect")
    require(fixture_links(other) == {"E"}, "The post without a topic must appear in other")
    free_series = one_section(tactile, "data-series", "새 촉각 시리즈")
    require(reading_order(free_series) == ["D"], "A new, undeclared series must render its post")
    print("PASS: numeric series order, missing order, topic membership, and undeclared series")

    tags = read_document(output / "tags" / "index.html")
    expected = {"policy": {"A", "B", "E"}, "행동 토큰": {"A", "C"}, "촉각": {"D", "E"}}
    for tag, ids in expected.items():
        href = find_tag_link(tags, tag).attrs.get("href", "")
        archive = read_document(target_file(output, href, baseurl))
        found = fixture_links(archive)
        require(found == ids, f"Tag {tag!r}: expected fixture links {sorted(ids)}, got {sorted(found)}")
    print("PASS: multiple tags, Korean tags, and generated native archive destinations")


def ignore_copy(_directory, names):
    return [name for name in names if name in COPY_EXCLUDES or name.startswith("_site")]


def check_fixtures(source: Path) -> None:
    require((source / "_config.yml").is_file(), f"Not a site source directory: {source}")
    with tempfile.TemporaryDirectory(prefix="research-notes-navigation-") as temp:
        temporary = Path(temp)
        fixture_source = temporary / "source"
        output = temporary / "output"
        shutil.copytree(source, fixture_source, ignore=ignore_copy, symlinks=True)
        add_fixtures(fixture_source)
        command = ["bundle", "exec", "jekyll", "build", "--source", str(fixture_source),
                   "--destination", str(output), "--config", str(fixture_source / "_config.yml"), "--trace"]
        print("Building isolated navigation fixtures with the caller's Bundler environment...", flush=True)
        subprocess.run(command, cwd=source, check=True)
        check_rendered_navigation(output, baseurl_from_config(fixture_source))
    print("PASS: fixture source and output removed; the original site was not changed")


def check_production(output: Path) -> None:
    require((output / "index.html").is_file(), f"Production build/index.html is missing: {output}")
    markers = [MARKER.encode(), FIXTURE_ROUTE.encode()]
    failures = []
    checked = 0
    # HTML, search data, feeds, sitemap, and other published text assets.
    suffixes = {".html", ".htm", ".json", ".xml", ".js", ".txt", ".rss", ".atom", ".webmanifest"}
    for path in output.rglob("*"):
        relative = path.relative_to(output).as_posix()
        if MARKER in relative or FIXTURE_ROUTE in relative:
            failures.append(relative)
        elif path.is_file() and path.suffix.lower() in suffixes:
            checked += 1
            content = path.read_bytes()
            if any(marker in content for marker in markers):
                failures.append(relative)
    require(not failures, "Navigation fixtures leaked into production: " + ", ".join(failures[:15]))
    print(f"PASS: no fixture paths or markers in {checked} production text assets")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Site source; defaults to the parent of scripts/.")
    parser.add_argument("--production-dir", type=Path,
                        help="Only inspect this existing production output for fixture leakage; do not build.")
    args = parser.parse_args()
    try:
        if args.production_dir is not None:
            check_production(args.production_dir.resolve())
        else:
            check_fixtures(args.source_root.resolve())
    except (AssertionError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
