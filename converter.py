from parser import Unit,Step,pars_store_area
from jinja2 import FileSystemLoader, Environment
import xml.etree.ElementTree as etree
import os


def create_direcories():
    try:
        os.makedirs('./course')
        os.makedirs('./course/about')
        os.makedirs('./course/assets')
        os.makedirs('./course/chapter')
        os.makedirs('./course/course')
        os.makedirs('./course/draft/vertical')
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

create_standart_file()






