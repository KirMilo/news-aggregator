https://www.rbc.ru/politics/
https://ria.ru/politics/

https://ria.ru/economy/
https://www.rbc.ru/economics/
https://www.rbc.ru/finances/

https://www.rbc.ru/technology_and_media/
https://lenta.ru/rubrics/science/

https://sportrbc.ru/
https://www.cybersport.ru/
https://www.championat.com/auto/

# План:
# Подключить postgres
# Подключить elasticsearch
# Подключить redis
# Сделать ручки


python ./src/manage.py makemigrations
python ./src/manage.py migrate
python ./src/manage.py search_index --rebuild

# Таким образом при .save() для модели, также обновится документ в elasticsearch. (Сделать только для новостей и пользователей)
