"""Reading the xml file."""
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class FileReader:
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_xml_file(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return root

class ReadFromHTMLTags:

    def scrape_from_html_form(self, html_tags, document_dict):
        soup = BeautifulSoup(html_tags, "html.parser")

        product_descriptions = soup.find_all("ul")
        for product_info in product_descriptions:
            for li in product_info.find_all("li"):
                strong_text = li.find("strong").text.strip() if li.find("strong") else ""
                remaining_text = li.get_text(strip=True).replace(strong_text, "").strip()
                
                if 'Kumaş Bilgisi' in strong_text:
                    document_dict['fabric'] = remaining_text
                elif 'Ürün Ölçüleri' in strong_text:
                    document_dict['product_measurements'] = remaining_text
                elif 'Model Ölçüleri' in strong_text:
                    document_dict['model_measurements'] = remaining_text
                elif 'Modelin üzerindeki' in remaining_text:
                    document_dict['sample_size'] = strong_text

        return document_dict