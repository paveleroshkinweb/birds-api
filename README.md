# Birds

Для работы приложения создайте отдельную базу данных и пользователя для нее. Для этого выполните

#### su postgres -c psql

а затем выполните команды:

#### CREATE USER ornithologist WITH PASSWORD 'ornithologist';
#### CREATE DATABASE bidrs_db;
#### GRANT ALL PRIVILEGES ON DATABASE bidrs_db TO ornithologist;

Теперь нужно создать таблицы в базе и заполнить их данными:

#### psql --host=localhost --port=5432 --dbname=birds_db --username=ornithologist --password --file='sql/roll_db.sql'

Посчитать сколько птиц определенного цвета:

#### psql --host=localhost --port=5432 --dbname=birds_db --username=ornithologist --password --file='sql/queries/bird_colors.sql'

Вычислить статистические данные о птицах:

#### psql --host=localhost --port=5432 --dbname=birds_db --username=ornithologist --password --file='sql/queries/birds_stat.sql'

Для того чтобы запустить сервер, вам необходимо выполнить:
#### virtualenv birds
#### source birds/bin/activate
#### pip install -r requirements.txt
#### chmod a+x api.py
#### ./api.py
