<h3>Что это такое</h3>
<p>Модуль – кусок кода, который можно использовать в другом коде. В самом простом случае это файл.
В любом проекте функциональность разбивается на куски, каждый кусок селится в свой модуль.</p>
<p>Всё, что устанавливается с помощью pip, представляет собой модули. Модули иерархические:
ты можешь импортировать модуль <code>markdown</code> и пользоваться им, не зная, что внутри он импортирует
ещё десяток других модулей: Питон сам всё разрулит.</p>
<h3>Как этим пользоваться</h3>
<p>Имя модуля совпадает с именем файла и должно быть нормальным именем переменной в Питоне: например, не содержать
знаков минуса.</p>
<p>Предположим, что есть папка <code>3_bars</code>, в ней файл <code>data_loaders.py</code> с таким содержанием:</p>
<pre><code>:::python
import csv
import json


def load_from_json(filepath):
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def load_from_csv(filepath):
    with open(filepath, 'r') as file_handler:
        return list(csv.reader(file_handler))
</code></pre>
<p>А рядом есть файл <code>bars.py</code>, в котором мы хотим загрузить данные из csv. Вот что в нём можно написать:</p>
<pre><code>:::python
from data_loaders import load_from_csv  # импортируем функцию из модуля


print(load_from_csv('bars.csv')
</code></pre>
<p>А можно так:</p>
<pre><code>:::python
import data_loaders  # импортируем модуль целиком


print(data_loaders.load_from_csv('bars.csv')  # используем функцию с указанием модуля
</code></pre>
<p>Есть ещё вариант <code>from data_loaders import *</code>, но он вне закона. Забудьте о нём.</p>
<h3>Запуск модуля как скрипта</h3>
<p>Когда Питон видит <code>import data_loaders</code>, он находит файл <code>data_loaders.py</code> и выполняет его. Реально выполняет:
если в нём есть код, он будет выполнен. Даже если это не просто объявления функций, а их вызов. Представим,
что когда мы писали код в <code>data_loaders.py</code>, мы его дебажили. Например, так:</p>
<pre><code>:::python
import json


def load_from_json(filepath):
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


print(load_from_json('test.json'))
</code></pre>
<p>Теперь если мы импортируем этот модуль (<code>import data_loaders</code>), девятая строка выполнится, файл загрузится и выведется
на экран. А ведь в <code>bars.py</code> это не нужно! Можно этот код удалить, но тогда будет неудобно дорабатывать функцию
<code>load_from_json</code>: при изменении надо будет добавлять отладочный принт, а потом удалять.</p>
<p>Вот правильный способ это обойти:</p>
<pre><code>:::python
import json


def load_from_json(filepath):
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


if __name__ == '__main__':
    print(load_from_json('test.json'))
</code></pre>
<p>Иф на девятой строке значит "выполняй меня только если файл запущен напрямую, а не импортирован".
Теперь при запуске <code>python data_loaders.py</code> будет выполняться дебажная загрузка кода, а
при импорте этого модуля – не будет. То, что надо.</p>
<p><code>__main__</code> – одна из переменных магических переменных. Их можно узнать по двойным подчёркиваниям по краям.
Такие переменные доступны всегда и Питон запишет нужные значения в них за нас. В <code>__main__</code> хранится название модуля,
из которого был импортирован данный модуль. Если модуль выполняется напрямую, Питон запишет в эту переменную
значение <code>__main__</code> (<a href="https://docs.python.org/3/library/__main__.html">доки</a>). Хитро, а?</p>
<h3>Подводные камни</h3>
<p>Главный подводный камень – рекурсивный импорт. Это если мы импортируем <code>data_loaders</code> из <code>bars</code>, а для <code>data_loaders</code>
нужен <code>bars</code>. Вот так:</p>
<pre><code>:::python
# bars.py
import data_loaders

# data_loaders.py
import bars
</code></pre>
<p>Бах! Всё сломается при запуске.</p>
<p>Иногда бывает ещё веселее: когда импорты замыкаются в трёх и более файлах. Типа того:</p>
<pre><code>:::python
# bars.py
import data_loaders

# data_loaders.py
import helpers

# helpers.py
import bars
</code></pre>
<p>Всё сломается так же, как в примере выше, но ещё и заставит поломать голову при починке.</p>
<p>Чинить такие случаи просто: разбивать код на максимально независимые модули. В примере выше, например,
файлу <code>helpers.py</code> зачем-то нужен <code>bars.py</code>. Так быть не должно: в <code>helpers.py</code> должны жить
максимально независимые общие функции, которые используются в других файлах. Не наоборот.</p>
<h3>Как работает под капотом</h3>
<p>Важнее всего знать, как Питон выбирает файлы для импорта. Сначала он ищет подходящие файлы в рабочей директории,
рядом с <code>bars.py</code>. Если не находит, то проходит по папкам в <code>sys.path</code> и ищет нужный файл.</p>
<p>Иногда бывает так, что нужный модуль находится вне тех папок, которые обходит Питон. Один из вариантов побороть это
 – вручную добавить нужный путь в <code>sys.path</code> (это список). Но это на крайний случай, обычно есть более красивые способы.
Например, упаковать код в модуль и установить его с помощью pip. Так что тсс, я вам ничего не говорил.</p>
<p>В памяти все загруженные модули хранятся в <code>sys.modules</code>. Иногда встречаются случаи, когда файла нет, а модуль есть.
Это не сложно устроить:</p>
<pre><code>:::python
# mod.py
import sys
from types import ModuleType


dynamic_module = ModuleType(__name__)
dynamic_module.x = 5

sys.modules['some_weird_module'] = dynamic_module


# script.py
import mod  # тут выполнился код из mod.py
import some_weird_module  # модуль есть, а файла – нет


print(some_weird_module.x)  # 5
</code></pre>
<p>Делать так незаконно: это неочевидно, затрудняет отладку и вредит читаемости. Не надо так.</p>