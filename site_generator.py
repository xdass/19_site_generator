import jinja2
import markdown
import os
import json

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
    dict_config = load_json_config(';;;')
    topics_dir = 'topics'
    html_prfix = '.html'
    if not os.path.exists(topics_dir):
        os.mkdir(topics_dir)
    for article in dict_config['articles']:
        path = os.path.join(topics_dir, os.path.split(article['source'])[0])
        os.makedirs(path, exist_ok=True)
        html = convert_markdown_to_html(os.path.abspath(os.path.join('articles', article['source'])))
        topic_path = os.path.splitext(article['source'])[0]
        full_path = os.path.abspath(os.path.join(topics_dir, topic_path + html_prfix))
        with open(os.path.abspath(full_path), 'w', encoding='utf-8') as file:
            file.write(html)


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


