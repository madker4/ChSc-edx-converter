from parser import Unit,Step,pars_store_area
from jinja2 import FileSystemLoader, Environment
import os
import random as rand


def create_direcories():
    try:
        os.makedirs('./course')
        os.makedirs('./course/about')
        os.makedirs('./course/assets')
        os.makedirs('./course/chapter')
        os.makedirs('./course/course')
        os.makedirs('./course/html')
        os.makedirs('./course/policies/course')
        os.makedirs('./course/sequential')
        os.makedirs('./course/static')
        os.makedirs('./course/vertical')
        os.makedirs('./course/video')
    except OSError:
        pass


def create_standart_file():
    loader = FileSystemLoader('./template')
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    course_tmpl = env.get_template('course.xml')
    cc = course_tmpl.render(org_name='ChSc', course_num='CS9999')
    with open('course/course.xml', 'w') as f:
        f.write(cc)


def url_generate():
    word = list('qwertyuioplkjhgfdsazxcvbnm741852963')
    rand.shuffle(word)
    url = ''
    for x in range(32):
        url = url + rand.choice(word)
    return url


create_standart_file()
units, titles = pars_store_area()
loader = FileSystemLoader('./template')
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
course_tmpl = env.get_template('course/course.xml')
for i in titles:
    i['url'] = url_generate()
cc = course_tmpl.render(chapters=titles)
with open('course/course/course.xml', 'w') as f:
    f.write(cc)







