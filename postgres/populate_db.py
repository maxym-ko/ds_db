import sys
sys.path.append('../')

from generate_fake_data import generate_fake_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Resume, Hobby, PreviousJob, Base

DATABASE_URL = "postgresql://user:postgres@localhost/hr_system"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake_data = generate_fake_data()

hobbies_dict = {}

for hobby in {hobby for user in fake_data for hobby in user["resume"]["hobbies"]}:
    hobby_obj = Hobby(name=hobby)
    session.add(hobby_obj)
    hobbies_dict[hobby] = hobby_obj
session.commit()

for user_data in fake_data:
    user = User(
        login=user_data["login"],
        password=user_data["password"]
    )
    session.add(user)
    session.commit()

    resume = Resume(
        user_id=user.id,
        resume_title=user_data["resume"]["resume_title"]
    )
    user.resume = resume
    session.add(resume)

    for hobby in user_data["resume"]["hobbies"]:
        resume.hobbies.append(hobbies_dict[hobby])

    for job in user_data["resume"]["previous_jobs"]:
        previous_job = PreviousJob(
            resume_id=resume.id,
            city=job["city"],
            institution_name=job["institution_name"]
        )
        resume.previous_jobs.append(previous_job)

    session.commit()

for user in session.query(User).all():
    print(f'ID: {user.id}, Login: {user.login}, Password: {user.password}')

session.close()
