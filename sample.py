import requests
import json


def main():
    # エンドポイント
    url = 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=221-0866'
    # リクエスト
    res = requests.get(url)
    # 取得したjsonをlists変数に格納
    lists = json.loads(res.text)

    print(lists)


if __name__ == "__main__":
    main()