import xml.etree.ElementTree as ET
from xml.dom import minidom


def process_xml_file(input_file, output_file, search_term):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Define namespaces
    ns = {'mlat': 'http://mlat.uzh.ch/2.0', 'cc': 'http://mlat.uzh.ch/2.0'}

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for search_result in root.findall('.//mlat:search_result', namespaces=ns):
            # Check if any 'lb' tag has type='verse'
            verse_lines = search_result.findall('.//cc:lb[@type="verse"]', namespaces=ns)
            if verse_lines:
                author = search_result.find('mlat:author', namespaces=ns).text
                work = search_result.find('mlat:work', namespaces=ns).text
                year = search_result.find('mlat:decisive_year', namespaces=ns).text

                # Flag to check if we've written this entry
                entry_written = False

                # Collect all sentences in the result
                sentences = search_result.findall('.//mlat:sentence', namespaces=ns)
                for sentence in sentences:
                    sentence_xml = ET.tostring(sentence, encoding='unicode')
                    sentence_dom = minidom.parseString(sentence_xml)

                    lines = []
                    for node in sentence_dom.documentElement.childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            lines.append(node.data.strip())
                        elif node.nodeName == 'cc:lb' and node.attributes.get('type', '').value == 'verse':
                            lines.append('')  # New line for <cc:lb type="verse">

                    sentence_text = ' '.join(lines)
                    if search_term in sentence_text:
                        if not entry_written:  # Write author, work, year only once
                            out_file.write(f"{author}, {work}, {year}")
                            entry_written = True

                        match_index = next((i for i, line in enumerate(lines) if search_term in line), None)
                        if match_index is not None:
                            start = max(0, match_index - 1)
                            end = min(len(lines), match_index + 2)

                            # Write the lines with a newline
                            for line in lines[start:end]:
                                if line:  # Only write non-empty lines
                                    out_file.write(f"\n{line}")
                            out_file.write("\n\n")  # Add two newlines after each set of verse lines



input_xml = 'Abia_search.XML'  # Replace with your actual XML file name
search_word = 'Abia'
output_txt = f'{search_word}_results.txt'

process_xml_file(input_xml, output_txt, search_word)