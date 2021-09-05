import scrapy
from barcodesdatabase.tools import decode_email

class BarcodesSpier(scrapy.Spider):

    name = 'barcodes'

    start_urls = [
        'https://barcodesdatabase.org/fr/selected-products/?country_list_select=DZ&sort_options=date_descending',
        ]

    def parse(self, response):

        # Since there's only one table, we will get it's body
        table_body = response.css('tbody')
        # get rows
        rows = table_body.css('tr')

        for row in rows:
            # get columns
            cols = row.css('td')

            # extract attribute from the columns
            barcode = cols[0].css('::text').get()
            title = cols[1].css('::text').get()
            subtitle = cols[2].css('::text').get()
            description = cols[3].css('::text').get()

            fab_infos = cols[4].css('p')
            fab_name = fab_infos[0].css('::text').get()
            fab_phone_adress = fab_infos[2].css('::text').get()
            fab_encdoded_email = fab_infos[3].xpath('a/@data-cfemail').get()
            fab_email = decode_email(fab_encdoded_email)

            size_color = cols[5].css('::text').get()
            image = cols[6].css('::text').get()
            price = cols[7].css('::text').get()
            currency = cols[8].css('::text').get()

            # return item
            yield {
                'barcode': barcode,
                'title': title,
                'subtitle': subtitle,
                'description': description,
                'manufacturer_name': fab_name,
                'manufacturer_phone_adress': fab_phone_adress,
                'manufacturer_email': fab_email,
                'size_color': size_color,
                'image': image,
                'price': price,
                'currency': currency,
            }

        # scrape the next page if exists
        href = response.xpath("//a[contains(text(), '>')]/@href").get().replace('?', '&')
        if href:
            next_page_url = self.start_urls[0]+href
            yield scrapy.Request(next_page_url)