# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class Unit:

    def __init__(self, name, description,order):
        self.name = name
        self.description = description
        self.order = order
        self.step_list = list()
        self.attachment = dict()

    def add_step(self, step):
        self.step_list.append(step)

    def add_attachment(self, precis, manual):
        self.attachment = {'precis_link': precis,
                           'manual_link': manual}

    def sorting(self):
        self.step_list = sorted(self.step_list, key=lambda x: x.counter)

    def __str__(self):
        unit = {'name': self.name.encode('utf-8'),
                'description': self.description,
                'step_list': [str(s) for s in self.step_list]}
        return str(unit)


class Step:
    def __init__(self, name, type_step, link, visible_name, tags, counter):
        self.name = name
        self.type = type_step
        self.link = link
        self.visible_name = visible_name
        self.tags = tags
        self.counter = int(counter)

    def __str__(self):
        step = {'name': self.name,
                'type': self.type,
                'link': self.link,
                'visible_name': self.visible_name,
                'tags': self.tags,
                'counter': self.counter}
        return str(step)


def pars_store_area():
    f = open('storeArea.html', 'r')
    soup = BeautifulSoup(f, 'html.parser')
    units_tags = soup.find_all('div', attrs={
        'tags': '[[Окружающий мир. 1й класс]] unit'})
    unit_all = list()
    for unit in units_tags:
        unit_all.append(Unit(name=unit['title'],
                             description=unit.pre.text,
                             order=unit['oms']))
    for unit in unit_all:
        tags = '[[' + unit.name + ']] unitStep'
        steps_tag = soup.find_all('div', attrs={'tags': tags})
        for st in steps_tag:
            count = st['ordercounter']
            text = st.pre.text
            param = unicode(text).strip().split('\n')
            for p in param:
                param_str = p.split(u'|')
                if param_str[1] == u'ссылка на контент шага':
                    link = param_str[2]
                if param_str[1] == u'тип шага':
                    type_step = param_str[2]
                if param_str[1] == u'visibleName':
                    visible_name = param_str[2]
            step = Step(name=st['title'], type_step=type_step, link=link,
                        visible_name=visible_name, tags=tags, counter=count)
            unit.add_step(step)
        tags_att = '[[' + unit.name + ']] attachment'
        attach_tags = soup.find_all('div', attrs={'tags': tags_att})
        for attach in attach_tags:
            text = attach.pre.text
            param_att = unicode(text).strip().split('\n')
            for p in param_att:
                param_str = p.split(u'|')
                if param_str[1] == u'ссылка на материал':
                    if attach['title'].endswith(u'm'):
                        manual = param_str[2]
                    else:
                        precis = param_str[2]
        unit.add_attachment(precis=precis[2:], manual=manual[2:])
    unit_sort = sorted(unit_all, key=lambda unit: unit.order)
    title_tags = soup.find_all('div', attrs={
        'tags': '[[Окружающий мир. 1й класс]] [[заголовок 1 надуровня]]'})
    title_list = list()
    for t in title_tags:
        title = {'name': t['title'],
                 'num': t['oms']}
        title_list.append(title)
    title_list = sorted(title_list, key=lambda title: int(title['num']))
    return unit_sort, title_list

pars_store_area()


# def sobr_stor():
#     f = open('/home/madker4/Документы/курсы пам/дети и наука фул/standalone.html','r')
#     soup = BeautifulSoup(f, 'html.parser')
#     body = soup.body.find(id='storeArea')
#     # tags = re.compile('Окружающий мир\. 1й класс')
#     # store = body.find_all(tags = re.compile(u'Окружающий мир\. 1й класс'))
#     wr = open('storeArea.html', 'a')
#     wr.write(str(body))
#     # for s in store:
#     #     wr.write(str(s))
#
# sobr_stor()







