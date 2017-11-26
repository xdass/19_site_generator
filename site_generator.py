import os
import json
from collections import defaultdict
import jinja2
import markdown


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
    #dd = defaultdict(list)
    dict_config = load_json_config(';;;')
    topics_dir = 'topics'
    html_prefix = '.html'
    if not os.path.exists(topics_dir):
        os.mkdir(topics_dir)
    for article in dict_config['articles']:
        #dir_path = os.path.join(topics_dir, os.path.split(article['source'])[0])
        print(create_paths(article, topics_dir))
        #os.makedirs(dir_path, exist_ok=True)
        #path_to_md_file = os.path.abspath(os.path.join('articles', article['source']))
        #html = convert_markdown_to_html(path_to_md_file)
        #md_filename = os.path.split(path_to_md_file)[1]
        #html_filename = os.path.splitext(md_filename)[0] + html_prefix
        #path_to_html_file = os.path.join(*(os.getcwd(), dir_path, html_filename))
        #dd[article['topic']].append(path_to_html_file)
        # with open(os.path.abspath(path_to_html_file), 'w', encoding='utf-8') as file:
        #     file.write(html)


def create_paths(article, output_dir):
    html_prefix = '.html'
    dir_path = os.path.join(output_dir, os.path.split(article['source'])[0])
    path_to_md_file = os.path.abspath(os.path.join('articles', article['source']))
    md_filename = os.path.split(path_to_md_file)[1]
    html_filename = os.path.splitext(md_filename)[0] + html_prefix
    path_to_html_file = os.path.join(*(os.getcwd(), dir_path, html_filename))
    return output_dir, path_to_md_file, path_to_html_file


def create_index():
    index_template = env.get_template('index.html')
    r = index_template.render(
        {
            'topics': [
                {
                    "slug": "tutorial",
                    "title": "Арсенал"
                },
                {
                    "slug": "python_basics",
                    "title": "Основы Питона"
                },
                {
                    "slug": "html",
                    "title": "HTML"
                },
                {
                    "slug": "git",
                    "title": "Гит"
                }
            ]
        })
    print(r)

create_articles_catalog()

