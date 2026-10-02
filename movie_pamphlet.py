import unicodedata


_PAMPHLET_ART = {
    "배트맨": r"""
      /\       /\
     /  \_____/  \
 ___/             \___
/   /  /\     /\  \   \
\__/__/  \___/  \__\__/
       \_/   \_/
         `---'""",
    "어벤져스": r"""
       /\
      /  \
     / /\ \
    / /__\ \
   / /----\ \
  /_/      \_/
""",
    "터미네이터": r"""
     .--------.
    | @      @ |
    |  .----.  |
    |  |____|  |
    | |||||||| |
     \________/""",
    "탑건": r"""
       /\
      /  \
 ___/ /\ \___
/___/____\___\
    /|    |\
   /_|____|_\
      /  \
      \__/""",
}

_FALLBACK_ART = r"""
      .---.
     ( o o )
      |___|
     /|   |\
      `---'"""


def _display_width(text):
    return sum(2 if unicodedata.east_asian_width(char) in "FWA" else 1 for char in text)


def _art_for(movie):
    return _PAMPHLET_ART.get(movie, _FALLBACK_ART).strip("\n").splitlines()


def _framed_lines(title, movie, content_width=None):
    art = _art_for(movie)
    width = max(_display_width(line) for line in [title, *art])
    if content_width is not None:
        width = max(width, content_width)

    lines = ["+" + "-" * (width + 2) + "+"]
    for line in [title, "", *art]:
        padding = width - _display_width(line)
        lines.append(f"| {line}{' ' * padding} |")
    lines.append("+" + "-" * (width + 2) + "+")
    return lines


def print_movie_menu(movies):
    print("영화 목록:")
    for start in range(0, len(movies), 4):
        group = movies[start:start + 4]
        titles = [f"{start + index + 1}. {movie}" for index, movie in enumerate(group)]
        content_width = max(
            _display_width(line)
            for title, movie in zip(titles, group)
            for line in [title, *_art_for(movie)]
        )
        boxes = [
            _framed_lines(title, movie, content_width)
            for title, movie in zip(titles, group)
        ]
        max_height = max(len(box) for box in boxes)
        for box in boxes:
            box[-1:-1] = [
                f"| {' ' * content_width} |"
                for _ in range(max_height - len(box))
            ]
        for row in zip(*boxes):
            print("   ".join(row))
        print()


def print_movie_pamphlet(movie):
    title = f"영화 팜플렛: {movie}"
    for line in _framed_lines(title, movie):
        print(line)
    print()
