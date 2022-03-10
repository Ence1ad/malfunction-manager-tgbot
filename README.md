# Avanta_bot
!!!регистрируем порт nginx на сервере aws вкладка "Network&Security" => Security group
выбираем сервер добавляем rules PORT:80 HTTP!!!

В .env.prod указываем IP сервера вместо localhost
Меняем Debug=0

Для входа на сервер пишем в командную строку 
$ssh -i "C:\имя ключа(с расширением <.pem>" ubuntu@номер Ip #! регистрируем на сервере aws по ключу

(если возникла ошибка необходимо на ключе удалить лишний доступ пользователей)
свойства --> безопасность --> дополнительно --ды
> отключить наследование --> добавить --> выбрать субьект --> вводим адрес эл почты от windows (Chebura6ka@outlook.com) далее ok ok ok

(Либо используем программу MobaXterm:
добавляем номер ip
вставляем ключ ssh
в терминале пишем логин: ubuntu)

Обновляем сервер:
$sudo apt update && apt upgrade

Cтавим докер и докер-композ на сервер:
$sudo apt install docker docker-compose

Для копии наших файлов вводим команду В ЛОКАЛЬНОМ ТЕРМИНАЛЕ Pycharm:
$scp -i C:\имя ключа(с расширением <.pem> -r C:\дирекция с папкой проекта ubuntu@номер Ip:/home/ubuntu

При появлении проблем с пакетами(optional)
$sudo python3 -m pip install --upgrade requests

Даем права на запуск entrypoint перед стартом docker-compose
$chmod +x app/entrypoint.prod.sh

для запуска дdocker-compose заходим в директорию где находится файл (используй команду ls и $cd)  и вводим в кoнсоль:
$sudo docker-compose -f docker-compose.prod.yml up -d --build  #! запуск файла продакшен

вход в консоль контейнера (нажимаем ctrl-z)
$sudo docker exec -it (имя контейнера) bash
или
$sudo docker exec -it (имя контейнера) sh


создаем супер пользователя
python manage.py createsuperuser

Используем shall для предварительной загрузки db данными (см файл fill db)

В интерфейсе оборудования импортируем таблицу с файла Equipment_db.xlsx
