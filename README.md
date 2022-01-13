###Запуск проекта
* git clone https://github.com/zm412/correlationTest.git
* docker-compose build
* docker-compose up
* docker-compose exec web sh
	$ python manage.py migrate
* приложение должно запуститься по адресу 0.0.0.0:8000
* регистрация
* в нижней части страницы, следует создать пару типов (например, 'steps', 'pulse', 'running')
* после этого, можно собирать данные на отправку (Str x, Str y - названия типов, далее, следует вводить дату и значение. Кнопка Add line добавляет еще один набор инпутов, Collect info показывает собранные данные, Send Collection - отправляет набор по маршруту.
* Блок, расположенный ниже, позволяет собрать данные для гет запроса

