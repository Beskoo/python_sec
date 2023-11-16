import mechanize

def viewPage(url):
    browser = mechanize.Browser()
    page = browser.open(url)
    print("*" * 16 + " PAGE HTML " + "*" * 16)
    source_code = page.read()