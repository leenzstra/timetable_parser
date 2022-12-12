import lxml.html as html
import requests
from models import Group
from typing import List

url = 'https://pstu.ru/student/new_timetable/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

s = requests.Session()
s.headers.update(headers)

def parse_table_groups() -> List[Group]:
    res = s.get(url)
    tree = html.fromstring(res.text)
    facultys = tree.xpath('.//div[@class = "content"]/div/a')
    groups = []

    for faculty in facultys:
        print(faculty.get('href'), faculty.text_content(), flush=True)
        faculty_url = url + faculty.get('href')

        for gr in parse_directions(faculty_url):
            gr.faculty = faculty.text_content()
            groups.append(gr)

    return groups


def parse_directions(faculty_url) -> List[Group]:
    res = s.get(faculty_url)
    tree = html.fromstring(res.text)
    directions = tree.xpath(
        './/div[@class = "content"]/div[@style = "padding:3px 5px 3px 25px"]/a')
    groups = []

    for direction in directions:
        # print(direction.get('href'), direction.text_content())
        direction_url = url+direction.get('href')
        for gr in parse_groups(direction_url):
            gr.direction = direction.text_content()
            groups.append(gr)

    return groups


def parse_groups(direction_url) -> List[Group]:
    res = s.get(direction_url)
    tree = html.fromstring(res.text)
    groups_node = tree.xpath(
        './/div[@class = "content"]/div[@style = "padding:3px 5px 3px 45px"]/a')
    groups = []

    for group in groups_node:
        group_url = url+group.get('href')
        # groups.append(Group(None, None, group.text_content(), group_url))
        for gr in parse_files(group_url):
            gr.group_name = "".join(str(group.text_content()).split())
            groups.append(gr)
            print(gr.group_name)

    return groups


def parse_files(group_url) -> List[Group]:
    res = s.get(group_url)
    tree = html.fromstring(res.text)
    files = tree.xpath(
        './/div[@class = "content"]/div[@style = "padding:3px 5px 3px 65px"]/a')
    groups = []

    for file in files:
        #print(file.get('href'), file.text_content())
        groups.append(
            Group(None, None, None, file.get('href'), file.text_content()))

    return groups
