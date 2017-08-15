# -*- coding: utf-8 -*-
from parser import Unit,Step,pars_store_area
from jinja2 import FileSystemLoader, Environment
import os
import random as rand
import shutil as sh


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


def write_file(name, template):
    with open(name, 'w') as f:
        f.write(template.encode('utf-8'))


def create_standart_file(env):
    course_tmpl = env.get_template('course.xml')
    tmplt = course_tmpl.render(org_name='ChSc', course_num='CS9999')
    write_file('course/course.xml', tmplt)


def url_generate():
    word = list('qwertyuioplkjhgfdsazxcvbnm741852963')
    rand.shuffle(word)
    url = ''
    for x in range(32):
        url = url + rand.choice(word)
    return url


def create_course_xml(env, titles):
    course_tmpl = env.get_template('course/course.xml')
    tmplt = course_tmpl.render(chapters=titles, name='ChildSci')
    write_file('course/course/course.xml', tmplt)


def create_chapters(env, titles, units):
    chapt_tmplt = env.get_template('chapter.xml')
    title_len = len(titles)
    for u in units:
        for t in range(0, title_len-1):
            if titles[t]['num'] < u.order < titles[t + 1]['num']:
                u.url = url_generate()
                titles[t]['units_url'].append(u.url)
                break
        if titles[title_len-1]['num'] < u.order:
            u.url = url_generate()
            titles[title_len-1]['units_url'].append(u.url)
    for t in titles:
        chapt = chapt_tmplt.render(t)
        name_file = 'course/chapter/' + t['url'].encode('utf-8') + '.xml'
        write_file(name_file, chapt)


def create_seq(env, units):
    seq_tmpl = env.get_template('sequential.xml')
    for u in units:
        for s in u.step_list:
            s.url = url_generate()
        seq = seq_tmpl.render(name=u.name[3:].strip().replace('&nbsp;',' '), step_list=u.step_list)
        name_file = 'course/sequential/' + u.url.encode('utf-8') + '.xml'
        write_file(name_file, seq)
        create_vertical(env, u.step_list)
        copy_attachment('/home/madker4/Документы/курсы пам/дети и наука фул/',
                        u)


def create_vertical(env, step_list):
    vert_tmpl = env.get_template('vertical.xml')
    for s in step_list:
        s.url_block = url_generate()
        if s.type == u'video':
            type_block = s.type
        elif s.type == u'pager':
            type_block = 'html'
        else: type_block = 'task'
        vert = vert_tmpl.render(name=s.visible_name.replace('&nbsp;', ' '),
                                type=type_block, url=s.url_block)
        name_file = 'course/vertical/' + s.url.encode('utf-8') + '.xml'
        write_file(name_file, vert)
        create_block(env, s)
        copy_pager_file('/home/madker4/Документы/курсы пам/дети и наука фул/',
                        s)


def create_block(env, step):
    if step.type == u'video':
        create_video_block(env, step)
    elif step.type == u'pager':
        create_html_block(env, step)


def create_video_block(env,step):
    video_tmpl = env.get_template('video.xml')
    video = video_tmpl.render(url=step.link.split('/')[-1],
                              block_url=step.url_block,
                              name=step.visible_name.replace('&nbsp;', ' '))
    name_file = 'course/video/' + step.url_block.encode('utf-8') + '.xml'
    write_file(name_file, video)


def create_html_block(env, step):
    html_tmpl = env.get_template('/html/block.html')
    xml_tmpl = env.get_template('/html/block.xml')
    html = html_tmpl.render(img_name=step.link.split(u'/')[-1])
    xml = xml_tmpl.render(name=step.visible_name.replace('&nbsp;', ' '),
                          block_url=step.url_block)
    name_html = 'course/html/' + step.url_block.encode('utf-8') + '.html'
    name_xml = 'course/html/' + step.url_block.encode('utf-8') + '.xml'
    write_file(name_html, html)
    write_file(name_xml, xml)


def copy_pager_file(path_course, step):
    if step.type == u'pager':
        full_file_name = path_course + step.link.encode('utf-8')
        if os.path.isfile(full_file_name):
            sh.copy(full_file_name, './course/static')


def copy_attachment(path_course, unit):
    manual_name = path_course + unit.attachment['manual_link'].encode('utf-8')
    precis_name = path_course + unit.attachment['precis_link'].encode('utf-8')
    if os.path.isfile(manual_name):
        sh.copy(manual_name, './course/static')
    if os.path.isfile(precis_name):
        sh.copy(precis_name, './course/static')


create_direcories()
units, titles = pars_store_area()
loader = FileSystemLoader('./template')
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
for i in titles:
    i['url'] = url_generate()
    i['units_url'] = list()
create_standart_file(env)
create_course_xml(env, titles)
create_chapters(env, titles, units)
create_seq(env, units)












