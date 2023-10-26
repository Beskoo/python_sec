import requests

r = requests.get("https://bing.com")

print(r.text)
print(r.headers)
for cookie in r.cookies:
    print(cookie)