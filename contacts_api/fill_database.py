from datetime import datetime
from random import randint, choice
from faker import Faker


from src.db.db import DBSession
from src.db.models import Contact, User


COUNT_CONTACTS = 100

fake = Faker()



def fill_contacts_table():
    unique_phones = []
    generated_contacts = []

    
    step = 0
    while True:
        if step == COUNT_CONTACTS:
            break
        
        phone = f"380{choice(['50', '66', '98', '68', '63'])}{randint(10**6, (10**7)-1)}"
        
        if phone in unique_phones:
            continue
        
        unique_phones.append(phone)
        step += 1

    with DBSession() as db:

        users = db.query(User).all()
        COUNT_USERS = len(users)

        for i in range(COUNT_CONTACTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birthday = datetime(year=randint(1994, 2000), month=randint(1, 12), day=randint(1, 29)).date()
            email = f"{first_name}.{last_name}@{choice(['gmail.com', 'outlook.com', 'school.com', 'mail.com'])}"
            phone = unique_phones[i]
            favorite = choice([True, False])
            contact_owner_id = randint(1, COUNT_USERS)
            created_at = datetime.now()
            updated_at = datetime.now()

            contact = Contact(
                first_name=first_name,
                last_name=last_name,
                birthday=birthday,
                email=email,
                phone=phone,
                favorite=favorite,
                contact_owner_id=contact_owner_id,
                created_at=created_at,
                updated_at=updated_at
            )
            db.add(contact)
        db.commit()
        print('Database "Contacts" successfully filled!')

if __name__ == '__main__':
    fill_contacts_table()
