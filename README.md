# RealOrAI
## A mini web application / game where you need to distinguish AI-generated content from real
## Это мини веб приложение (игра) суть которой - отличать AI изображения от реальных.

Проект развернут на - http://84.201.180.190/signin


### Как использовать сервис?
* Для начала вам надо создать аккаунт в проекте, или войти в существующий. Перейдите по адресу http://84.201.180.190/signin. Если у вас еще нет аккаунта, нажмите "зарегистрироваться" внизу формы
* На главной странице вы видите рейтинговую таблицу. Новым участникам дается рейтинг 1500, после каждой игры он изменяется. Система подсчета рейтинга работает по системе Эло, в качестве противника выступает игра, у нее рейтинг всегда 1500
* На главной странице есть кнопка "начать игру", по нажатию на нее генерируется новая игра. Игра - это набор карточек (обычно их 10), на каждой карточке изображение, и надо угадать, реальное оно или нет (нажать на соответствующие кнопки внизу страницы). Игра может генерироваться несколько минут.
* После окончания игры будет показано количество правильных и неправильных ответов, а также насколько изменился рейтинг

## Как работает приложение?
При генерации новой игры 5 изображений берется из базы данных (это изображения от прошлых игр всех участников), 3 изображения берется из api случайных картинок https://picsum.photos/, и 2 картинки из нейросети YandexART (Янедкс Облако api), эти 2 картинки генерируются нейросетью каждый раз, поэтому загрузка игры может знаять какое-то время.

Примечание: если хотите запуситить приложение локально или развернуть его еще где-то, вам будет нужен токен от YandexCloud для генерации изображений через YandexART. Токен задается через переменные окружения (.env) значение YANDEX_API_TOKEN.
