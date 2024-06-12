from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models import User, Resume, Hobby, PreviousJob, resume_hobby

DATABASE_URL = "postgresql://user:postgres@localhost/hr_system"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def get_resume_of_user(user_login):
    result = session.query(Resume).join(User).filter(User.login == user_login).first()
    return result


def get_hobbies_of_user(user_login):
    result = (session.query(Hobby)
                     .join(resume_hobby)
                     .join(Resume)
                     .join(User)
                     .filter(User.login == user_login)
                     .all())
    return result


def get_all_hobbies():
    result = session.query(Hobby).distinct().all()
    return result


def get_all_cities():
    result = session.query(PreviousJob.city).distinct().all()
    return result


def get_hobbies_by_city(city_name):
    result = (session.query(Hobby)
                     .join(resume_hobby)
                     .join(Resume)
                     .join(PreviousJob)
                     .filter(PreviousJob.city == city_name)
                     .all())
    return result


def get_users_by_institution():
    subquery = (select(PreviousJob.institution_name).group_by(PreviousJob.institution_name)
                                                    .having(func.count(PreviousJob.id) > 1)
                                                    .subquery())
    users = (session.query(User)
                    .join(Resume)
                    .join(PreviousJob)
                    .filter(PreviousJob.institution_name.in_(subquery.select()))
                    .distinct()
                    .all())
    return users


if __name__ == "__main__":
    user_login = "qbaker"
    city_name = "Smithburgh"

    # 1. Забрати рюзюме конкретного працівника
    resume = get_resume_of_user(user_login)
    print(f"Resume of user {user_login}: {resume.resume_title}\n")

    # 2. Забрати всі хоббі які існують в резюме конкретного працівника
    hobbies_of_user = get_hobbies_of_user(user_login)
    print(f"Hobbies in resume of user {user_login}: {[hobby.name for hobby in hobbies_of_user]}\n")

    # 3. Забрати всі хоббі які існують в резюме усіх працівників
    all_hobbies = get_all_hobbies()
    print(f"All hobbies in resumes of all users: {[hobby.name for hobby in all_hobbies]}\n")

    # 4. Забрати всі міста, що зустрічаються в резюме усіх працівників
    all_cities = get_all_cities()
    print(f"All cities in resumes of all users: {[city[0] for city in all_cities]}\n")

    # 5. Забрати хоббі всіх працівників, що працювали в заданому місті
    hobbies_by_city = get_hobbies_by_city(city_name)
    print(f"Hobbies of users who worked in {city_name}: {[hobby.name for hobby in hobbies_by_city]}\n")

    # 6. Забрати всіх працівників, що працювали в одному закладі (заклад ми не вказуємо)
    users_by_institution = get_users_by_institution()
    print(f"Users who worked in the same institution: {set([user.login for user in users_by_institution])}")

    session.close()
