import xml.etree.ElementTree as et

NAMESPACE = {"mlat": "http://mlat.uzh.ch/2.0"}  # Define namespace


def extract_verse_entries(xml_file, search_term):
    tree = et.parse(xml_file)
    root = tree.getroot()

    output_file = f"{search_term}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for search_result in root.findall("mlat:search_result", NAMESPACE):
            sentence = search_result.find(".//mlat:sentence", NAMESPACE)

            # Debugging step
            if sentence is None:
                print("No <sentence> found in an entry.")
                continue  # Skip this entry

            # Check for verse formatting
            if sentence.findall(".//mlat:lb", NAMESPACE):
                author = search_result.find("mlat:author", NAMESPACE).text.strip()
                work = search_result.find("mlat:work", NAMESPACE).text.strip()
                year = search_result.find("mlat:decisive_year", NAMESPACE).text.strip()

                # Extract text and split lines based on <cc:lb/>
                text_lines = []
                current_line = ""
                for elem in sentence.iter():
                    tag = elem.tag.split("}")[-1]  # Remove namespace prefix
                    if tag == "lb":
                        text_lines.append(current_line.strip())  # Add previous line
                        current_line = ""
                    elif elem.text:
                        current_line += elem.text.strip() + " "
                if current_line.strip():
                    text_lines.append(current_line.strip())

                # Debugging output
                print(f"Processing entry: {author}, {work}, {year}")
                print("Extracted lines:", text_lines)

                # Find the search term in the text (case-insensitive)
                for i, line in enumerate(text_lines):
                    if search_term.lower() in line.lower():
                        before = text_lines[i - 1] if i > 0 else ""
                        after = text_lines[i + 1] if i < len(text_lines) - 1 else ""

                        # Write to file
                        f.write(f"{author}, {work}, {year}\n")
                        if before:
                            f.write(before + "\n")
                        f.write(line + "\n")  # The search term line
                        if after:
                            f.write(after + "\n")
                        f.write("\n")  # Space between entries
                        print(f"Match found! Writing to {output_file}")
                        break  # Stop after the first match



# Example usage
extract_verse_entries("Abia_search.xml", "Abia")
