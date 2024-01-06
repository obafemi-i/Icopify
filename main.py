from playwright.sync_api import sync_playwright, Playwright, Page
from selectolax.parser import HTMLParser
import time
import csv
import creds

CSV_file_name = 'Sample'

all_data = []

login_url = ('https://icopify.co/login')


def login(playwright: Playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    page.goto(login_url)

    page.fill('input#Email', creds.email)
    page.fill('input#password', creds.password)

    page.check('input#basic-checkbox')

    page.click('button[type=submit]')


    print('Succesfully logged in..')

    return page    


def parse_webiste_info(html: HTMLParser):
    website_data = html.css('tbody tr')
    for data in website_data:
        traffic = data.css('td')[2].text().replace('Monthly Traffic', '').strip()
        dr = data.css('td')[3].text().replace('DR', '').strip()
        price = data.css('td')[6].css('a')[1].text().strip().replace('$','')

        data_dict = {
            'Traffic': traffic,
            'DR': dr,
            'Price': price
        }

        all_data.append(data_dict)

        # print(data_dict)


def run_browser(login: Page):
    for x in range(1, 3):
        url = f'https://icopify.co/publishers?page={x}'


        login.goto(url)
        login.is_visible('td.align-middle')

        html = login.inner_html('div.table-responsive')
        body = HTMLParser(html)

        print(f'getting info from page {x}..')

        parse_webiste_info(body)



def export_to_csv(products: list):
    field_names = ['Traffic', 'DR', 'Price',]
    with open(f'{CSV_file_name}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(products)



def main():
    with sync_playwright() as playwright:
        login_page = login(playwright)
        run_browser(login_page)
        time.sleep(2)

    export_to_csv(all_data)


if __name__ == '__main__':
    main()
