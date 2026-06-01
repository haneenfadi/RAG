from bs4 import BeautifulSoup


def parse_lob(html):
    soup = BeautifulSoup(html, "html.parser")

    content = soup.select_one("p.DraftDetails")

    if content:
        text = content.get_text(separator="\n")
    else:
        text = "NOT FOUND"

    return {
        "text": text,
        "metadata": {
            "source": "lob.gov.jo",
            "type": "law",
            "language": "ar"
        }
    }
