from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Resume, Hobby, PreviousJob, Base
from faker import Faker

DATABASE_URL = "postgresql://user:postgres@localhost/hr_system"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

hobbies = [Hobby(name=faker.word()) for _ in range(20)]
session.add_all(hobbies)
session.commit()

users = []
for _ in range(100):
    user = User(
        login=faker.user_name(),
        password=faker.password()
    )
    session.add(user)
    session.commit()

    resume = Resume(
        user_id=user.id,
        resume_title=faker.job()
    )
    user.resume = resume
    session.add(resume)

    for hobby in faker.random_choices(elements=hobbies, length=5):
        resume.hobbies.append(hobby)

    for _ in range(4):
        previous_job = PreviousJob(
            resume_id=resume.id,
            city=faker.city(),
            institution_name=faker.company()
        )
        resume.previous_jobs.append(previous_job)

    session.commit()

for user in session.query(User).all():
    print(f'ID: {user.id}, Login: {user.login}, Password: {user.password}')

session.close()
