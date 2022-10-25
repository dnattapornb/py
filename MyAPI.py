import json
import requests
from bs4 import BeautifulSoup


class MyAPI:

    def __init__(self):
        self.rq = requests.Session()
        self.url = "https://rcm66.rta.mi.th/rcm66/66/rep/"
        self.rs = self.rq.get(self.url)
        # print(self.rs.cookies)

        self.url = 'https://rcm66.rta.mi.th/rcm66/66/rep/reportdata.php'
        self.data = {'action': 'statTP'}
        self.html = requests.post(self.url, cookies=self.rs.cookies, data=self.data)
        # print(self.html.text)

    def get(self):
        groups = []

        soup = BeautifulSoup(self.html.text, 'html.parser')
        # print(soup.prettify())

        boxs = soup.findAll('div', {'class': 'alert alert-warning'})
        for box in boxs:
            group = {
                'name': None,
                'lists': [],
            }
            group['name'] = box.find('font').find('strong').getText()
            # print(group['name'])
            contents = box.find('div', {'class': 'container-fluid'}).findAll('div', {'class': 'row mb-2'})
            for content in contents:
                rows = content.findAll('div')

                _ROW = []
                for row in rows:
                    _ROW.append(row.getText())
                # print(_ROW)

                i = 0
                list = {
                    'group': None,
                    '18-20': None,
                    '22-29': None,
                    'total': None,
                    'received': None,
                }
                for l in list:
                    list[l] = _ROW[i]
                    i += 1
                # print(list)

                group['lists'].append(list)
            groups.append(group)
        return json.dumps(groups)


if __name__ == '__main__':
    api = MyAPI()
    rs = api.get()
    print(rs)
    print(json.loads(rs)[0]['name'])
# rq = requests.Session()
# url = "https://rcm66.rta.mi.th/rcm66/66/rep/"
# rs = rq.get(url)
# # print(rs.cookies)
#
# url = 'https://rcm66.rta.mi.th/rcm66/66/rep/reportdata.php'
# data = {'action': 'statTP'}
# html = requests.post(url, cookies=rs.cookies, data=data)
# # print(html.text)
#
# soup = BeautifulSoup(html.text, 'html.parser')
# # print(soup.prettify())
#
# groups = []
# boxs = soup.findAll('div', {'class': 'alert alert-warning'})
# for box in boxs:
#     group = {
#         'name': None,
#         'lists': [],
#     }
#     group['name'] = box.find('font').find('strong').getText()
#     # print(group['name'])
#     contents = box.find('div', {'class': 'container-fluid'}).findAll('div', {'class': 'row mb-2'})
#     for content in contents:
#         rows = content.findAll('div')
#
#         _ROW = []
#         list = {
#             'group': None,
#             '18-20': None,
#             '22-29': None,
#             'total': None,
#             'received': None,
#         }
#         for row in rows:
#             _ROW.append(row.getText())
#         # print(_ROW)
#
#         i = 0
#         for l in list:
#             list[l] = _ROW[i]
#             i += 1
#         # print(list)
#
#         group['lists'].append(list)
#     groups.append(group)
# json_object = json.dumps(groups, indent=4)
# # print(json_object)
# # print(json.loads(json_object)[0]['name'])
# print("\n")
