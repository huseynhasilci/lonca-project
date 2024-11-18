"""Organize the document before inserting into db."""
from utils.helpers.FileReader import ReadFromHTMLTags

from constants.ApplicationConstants import (
    PRODUCT_KEYWORD,
    DISCOUNTED_PRICE_KEYWORD,
    PRODUCT_TYPE_KEYWORD,
    PRICE_UNIT_KEYWORD,
    DESCRIPTION_KEYWORD,
    IMAGE_PATH,
    PRODUCT_DETAIL_PATH,
)


class DocumentOrganizer:
    
    def __init__(self, root):
        self.root = root
        self.bulk_write_list = []
        self.html_tag_obj = ReadFromHTMLTags()


    def orginze_document(self):
        products = self.root.findall(PRODUCT_KEYWORD)

        for product in products:
            document_dict = {}

            is_discounted = False
            status = 'Active'

            product_id = product.get('ProductId')
            name = product.get('Name').title()

            document_dict['stock_code'] = product_id
            document_dict['name'] = name

            images = [image.get('Path') for image in product.findall(IMAGE_PATH)]

            document_dict['images'] = images

            product_details = product.findall(PRODUCT_DETAIL_PATH)

            for item in product_details:
                key = item.get('Name')

                if key == DISCOUNTED_PRICE_KEYWORD:
                    key = 'discounted_price'
                elif key == PRODUCT_TYPE_KEYWORD:
                    key = 'product_type'
                elif key == PRICE_UNIT_KEYWORD:
                    key = 'price_unit' 
                else:
                    key = key.lower()

                if key == 'color':
                    document_dict[key] = [item.get('Value')]
                else:
                    document_dict[key] = item.get('Value')

            if document_dict['price'] != document_dict['discounted_price']:
                is_discounted = True
            
            if document_dict['quantity'] == '0':
                status = 'Passive'

            document_dict['is_discounted'] = is_discounted
            document_dict['status'] = status

            product_description = product.find(DESCRIPTION_KEYWORD).text

            document_dict = self.html_tag_obj.scrape_from_html_form(product_description, document_dict)

            if '' not in document_dict:
                document_dict['price_unit'] = 'USD'

            self.bulk_write_list.append(document_dict)

        return self.bulk_write_list
