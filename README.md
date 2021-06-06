
<div align="center">
  <h1>Key Task</h1>
</div>

- **Clone**: `git clone https://github.com/guluzadef/Task_Passport`
- **After Clone**: `cd Key_History`

- **Create and Activate virtualenv**: `python3 -m venv venv`  **after** `source /venv/bin/activate`

- **Install requiremets**: `pip3 install -r requirements.txt`

- **Create Database** : `docker-compose up --build -d 
`

- **Migrate Database** : `python manage.py makemigrations` **after** `python manage.py migrate`

- **Run Project** : `python manage.py runserver`


