# todomvc-react-backend
To setup, run `scripts/install.sh`, then run `mysql -u root -p < scripts/create.sql` to init mysql database.

To run, do:
```shell
source venv/bin/activate
python src/main.py 8080
```

Demo: http://huumanoid.ru:8080

To enable websockets capability (realtime updates for simultaneous sessions), specify domain and port in `src/appconfig.py`
