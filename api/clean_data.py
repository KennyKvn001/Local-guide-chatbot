from bs4 import BeautifulSoup
import re
from collections import OrderedDict


def clean_text(text):
    # Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text(separator=" ", strip=True)

    # Remove image URLs and Markdown image syntax
    cleaned = re.sub(r"!\[.*?\]\(.*?\)", "", cleaned)
    cleaned = re.sub(r'https?://[^\s<>"\']+', "", cleaned)

    # Remove navigation links (e.g., [Tourism](...))
    cleaned = re.sub(r"\[.*?\]\(.*?\)", "", cleaned)

    # Remove extra whitespace and empty lines
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = "\n".join(line for line in cleaned.split("\n") if line.strip())

    return cleaned


def deduplicate_lines(text):
    # Split into lines, remove duplicates while preserving order
    lines = text.split("\n")
    return "\n".join(OrderedDict.fromkeys(lines))


def clean_rwanda_data(
    input_file="rwanda_data.txt", output_file="cleaned_rwanda_data.txt"
):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Split by source for processing
        sources = text.split("Source: ")[1:]  # Skip empty first split
        cleaned_text = ""

        for source in sources:
            # Extract source URL and content
            source_url, content = source.split("\n", 1)
            cleaned_content = clean_text(content)

            # Add source header and cleaned content
            cleaned_text += f"Source: {source_url}\n{cleaned_content}\n\n"

        # Deduplicate lines across the entire text
        cleaned_text = deduplicate_lines(cleaned_text)

        # Save cleaned data
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print(f"Cleaned data saved to {output_file}")

    except Exception as e:
        print(f"Error cleaning data: {str(e)}")


if __name__ == "__main__":
    clean_rwanda_data()
