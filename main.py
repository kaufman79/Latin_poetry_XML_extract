import xml.etree.ElementTree as ET


def extract_verse_entries(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(output_file, "w", encoding="utf-8") as f:
        for search_result in root.findall("search_result"):
            sentence = search_result.find(".//sentence")

            # Check if there are <cc:lb/> elements, indicating verse
            if sentence is not None and sentence.find(".//{http://mlat.uzh.ch/2.0}lb") is not None:
                author = search_result.find("author").text.strip()
                work = search_result.find("work").text.strip()
                year = search_result.find("decisive_year").text.strip()

                # Extract the Latin text, splitting lines at <cc:lb/>
                text_lines = [text.strip() for text in sentence.itertext() if text.strip()]

                # Write to file
                f.write(f"{author}, {work}, {year}\n")
                for line in text_lines:
                    f.write(f"{line}\n")
                f.write("\n")  # Add space between entries


extract_verse_entries("input.xml", "output.txt")
