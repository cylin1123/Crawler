import requests

def main(text):

    response = requests.get("https://www.google.com.tw/search?q=%s"%('zzz'))

    if response.status_code == 200 :
        print(response.text)
        print(response.context)


if __name__ =="__main__":
    main("AAA")