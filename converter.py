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
    policies_tmpl = env.get_template('./policies/course/policy.json')
    tmplt = course_tmpl.render(org_name='ChSc', course_num='CS9999')
    policy = policies_tmpl.render()
    write_file('course/course.xml', tmplt)
    write_file('course/policies/course/policy.json', policy)


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
        t['name'] = t['name'].replace('&nbsp;',' ')
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
        elif s.type == u'task':
            create_task_block(env, s)
            continue
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


def create_task_block(env, step):
    task_tmpl = env.get_template('task.xml')
    source_name = step.visible_name.replace('&nbsp;', '_').replace(' ', '_').replace('?', '_',)
    source = source_name + '.html'
    task = task_tmpl.render(block_url=url_generate(),
                            name=step.visible_name.replace('&nbsp;', ' '),
                            source=source)
    name_file = 'course/vertical/' + step.url.encode('utf-8') + '.xml'
    print name_file
    write_file(name_file, task)
    copy_task_file(step)


def copy_task_file(step):
    task_dir = '/home/madker4/Документы/курсы пам/дети и наука фул/' + step.link[:-10].encode('utf-8')
    task_file = open(task_dir + 'index.html','r') #добавить проверку существования файла
    task_lines = task_file.readlines()
    for index, value in enumerate(task_lines):
        if value.find('../../_Commons/widgets/1.0.1/style.css') > 0:
            task_lines[index] = value.replace('../../_Commons/widgets/1.0.1/', '')
            continue
        elif value.find('../../_Commons/widgets/1.0.1/production.min.js') > 0:
            task_lines[index] = value.replace('../../_Commons/widgets/1.0.1/', '')
            continue
        elif value.find('url(images/') > 0:
            task_lines[index] = value.replace('url(images/', 'url(')
    name_file = 'course/static/' + step.visible_name.replace('&nbsp;', ' ') + '.html'
    new_task_file = open(name_file, 'w')
    for line in task_lines:
        new_task_file.write(line)
    copy_task_img(task_dir)


def copy_task_img(task_dir):
    img_dir = task_dir + 'images/' #проверка существования папки
    if not os.path.isdir(img_dir):
        return None
    img_list = os.listdir(img_dir)
    for img in img_list:
        sh.copy(img_dir + img, './course/static')


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
    copy_task_lib()


def copy_task_lib():
    path = '/home/madker4/Документы/курсы пам/дети и наука фул/_Commons/widgets/1.0.1/'
    sh.copy(path + 'style.css', './course/static')
    sh.copy(path + 'production.min.js', './course/static')


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
