import xml.etree.ElementTree as ET

NAMESPACE = {"mlat": "http://mlat.uzh.ch/2.0"}  # Namespace handling


def debug_extraction(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    print("Looking for 'search_result' elements...")
    results = root.findall("mlat:search_result", NAMESPACE)

    if not results:
        print("No search results found! Check namespace handling.")
        return

    for result in results:
        print("\n=== Found search_result ===")

        sentence = result.find(".//mlat:sentence", NAMESPACE)

        if sentence is None:
            print("❌ No <sentence> found in this entry.")
            continue

        print("✔ <sentence> found:", sentence.text)

        # Check if this sentence contains <cc:lb/> tags (verse formatting)
        verse_breaks = sentence.findall(".//mlat:lb", NAMESPACE)

        if verse_breaks:
            print("✔ <cc:lb/> elements found! This is a verse entry.")
        else:
            print("❌ No <cc:lb/> found. This is NOT a verse.")

        # Extract and print sentence content
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

        print("Extracted text lines:", text_lines)


# Run debugging
debug_extraction("Abia_search.xml")
