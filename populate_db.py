from app import app, db
from models import Sprint, Task, Person
from datetime import datetime, timedelta

def populate_db():
    with app.app_context():
        # Удаление существующих данных
        db.drop_all()
        db.create_all()

        # Создание тестовых данных для людей
        persons = [
            Person(name='Alice', position='Developer'),
            Person(name='Bob', position='Tester'),
            Person(name='Charlie', position='Project Manager'),
            Person(name='David', position='Developer'),
            Person(name='Eve', position='Designer')
        ]
        db.session.add_all(persons)
        db.session.commit()

        # Создание тестовых данных для спринтов
        now = datetime.utcnow()
        sprints = [
            Sprint(name='Sprint 1', start_date=now - timedelta(days=30), end_date=now - timedelta(days=20)),
            Sprint(name='Sprint 2', start_date=now - timedelta(days=19), end_date=now - timedelta(days=10)),
            Sprint(name='Sprint 3', start_date=now - timedelta(days=9), end_date=now)
        ]
        db.session.add_all(sprints)
        db.session.commit()

        # Создание тестовых данных для задач
        tasks = [
            Task(title='Setup project repository', description='Initialize the project repository with initial files', status='Done', sprint_id=sprints[0].id, person_id=persons[0].id, created_at=now - timedelta(days=29), in_progress_at=now - timedelta(days=28), done_at=now - timedelta(days=27)),
            Task(title='Create project documentation', description='Write the initial project documentation', status='Done', sprint_id=sprints[0].id, person_id=persons[2].id, created_at=now - timedelta(days=29), in_progress_at=now - timedelta(days=27), done_at=now - timedelta(days=26)),
            Task(title='Setup CI/CD pipeline', description='Set up continuous integration and continuous deployment pipeline', status='Done', sprint_id=sprints[0].id, person_id=persons[0].id, created_at=now - timedelta(days=29), in_progress_at=now - timedelta(days=26), done_at=now - timedelta(days=25)),
            Task(title='Design project logo', description='Create a logo for the project', status='Done', sprint_id=sprints[0].id, person_id=persons[4].id, created_at=now - timedelta(days=28), in_progress_at=now - timedelta(days=27), done_at=now - timedelta(days=26)),
            Task(title='Implement user authentication', description='Develop user authentication module', status='In Progress', sprint_id=sprints[1].id, person_id=persons[0].id, created_at=now - timedelta(days=18), in_progress_at=now - timedelta(days=16)),
            Task(title='Write unit tests for authentication', description='Create unit tests for the authentication module', status='To Do', sprint_id=sprints[1].id, person_id=persons[1].id, created_at=now - timedelta(days=18)),
            Task(title='Develop user profile page', description='Create the user profile page', status='To Do', sprint_id=sprints[1].id, person_id=persons[3].id, created_at=now - timedelta(days=17)),
            Task(title='Implement project task board', description='Develop the Kanban board for project tasks', status='Done', sprint_id=sprints[1].id, person_id=persons[3].id, created_at=now - timedelta(days=18), in_progress_at=now - timedelta(days=15), done_at=now - timedelta(days=10)),
            Task(title='Design UI for task board', description='Create the user interface design for the task board', status='Done', sprint_id=sprints[1].id, person_id=persons[4].id, created_at=now - timedelta(days=17), in_progress_at=now - timedelta(days=16), done_at=now - timedelta(days=14)),
            Task(title='Integrate third-party API', description='Integrate with third-party API for additional data', status='In Progress', sprint_id=sprints[2].id, person_id=persons[0].id, created_at=now - timedelta(days=8), in_progress_at=now - timedelta(days=7)),
            Task(title='Write integration tests', description='Create integration tests for the third-party API', status='To Do', sprint_id=sprints[2].id, person_id=persons[1].id, created_at=now - timedelta(days=8)),
            Task(title='Optimize database queries', description='Optimize queries to improve performance', status='To Do', sprint_id=sprints[2].id, person_id=persons[3].id, created_at=now - timedelta(days=7)),
            Task(title='Finalize project documentation', description='Complete the project documentation with all changes', status='To Do', sprint_id=sprints[2].id, person_id=persons[2].id, created_at=now - timedelta(days=6)),
            Task(title='Deploy project to production', description='Deploy the final version of the project to production', status='To Do', sprint_id=sprints[2].id, person_id=persons[2].id, created_at=now - timedelta(days=5))
        ]
        db.session.add_all(tasks)
        db.session.commit()

if __name__ == '__main__':
    populate_db()
    print("Database populated successfully!")
