from bs4 import BeautifulSoup
import json


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    content = soup.select(".elementor-accordion-item")
    if content:

        all_text = []
        for item in content:
            text = item.get_text(separator="\n", strip=True)
            all_text.append(text)

    else:
        text = "NOT FOUND"

    with open("src/data/extracted/social_security_faq.json", "w", encoding="utf-8") as f:
        json.dump(all_text, f, ensure_ascii=False, indent=4)

    return {
        "text": all_text,
        "metadata": {
            "source": "ssc.gov.jo",
            "type": "law",
            "language": "ar"
        }
    }
