import os
import json
from collections import defaultdict
import jinja2
import markdown
import shutil


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates')
)
template = env.get_template('template.html')


def convert_markdown_to_html(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        text = f.read()
    html = markdown.markdown(text)
    return html


def load_json_config(json_file):
    try:
        with open('config.json', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def create_articles_catalog():
    dd = defaultdict(list)
    dict_config = load_json_config(';;;')
    for article in dict_config['articles']:
        html_file_path, md_file_path = create_paths(article)
        html = convert_markdown_to_html(md_file_path)
        dd[article['topic']].append(html_file_path)
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html)
    print(dd)


def create_paths(article):
    html_prefix = '.html'
    path_to_md_file = os.path.join(config['paths']['md_articles'], article['source'])
    md_filename = os.path.split(path_to_md_file)[1]
    html_filename = os.path.splitext(md_filename)[0] + html_prefix
    path_to_html_file = os.path.join(
        config['paths']['root'],
        config['paths']['html_articles'],
        os.path.split(article['source'])[0],
        html_filename
    )
    return path_to_html_file, path_to_md_file


def create_site_structure(articles, paths):
    topics_path = os.path.join(config['paths']['root'], config['paths']['md_articles'])
    root = config['paths']['root']
    css_path = os.path.join(root, config['paths']['css'])
    js_path = os.path.join(root, config['paths']['js'])
    site_css = ''
    site_js = ''
    try:
        shutil.copytree(config['paths']['css'], css_path)
        shutil.copytree(config['paths']['js'], js_path)
        for article in config['articles']:
            dirs_path = os.path.split(article['source'])[0]
            os.makedirs(os.path.join('site/topics', dirs_path), exist_ok=True)
    except FileExistsError:
        pass


def create_index():
    index_template = env.get_template('index.html')

config = load_json_config('')
create_site_structure('', '')
create_articles_catalog()
