import os
import django
from datetime import date, timedelta

# הגדרת הסביבה של דג'נגו
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectTasks.settings')
django.setup()

from django.contrib.auth.models import User
from App1.models import Person, Task


def seed():
    print("מנקה נתונים ישנים...")
    # מחיקת כל המשימות הקיימות כדי להתחיל מחדש בלי כפילויות
    Task.objects.all().delete()

    print("מכין משתמשים ומשימות מורחבות...")

    # 1. יצירת/שליפת משתמשים (שימוש ב-get_or_create מונע את השגיאה שקיבלת)
    users_info = [
        {'username': 'manager1', 'role': 'ma', 'staff': 'sa'},
        {'username': 'worker_front', 'role': 'wo', 'staff': 'fr'},
        {'username': 'worker_back', 'role': 'wo', 'staff': 'ba'},
        {'username': 'worker_ux', 'role': 'wo', 'staff': 'ux'},
    ]

    user_objs = {}
    for info in users_info:
        # get_or_create בודק אם המשתמש קיים. אם כן - הוא שולף אותו. אם לא - הוא יוצר.
        user, created = User.objects.get_or_create(username=info['username'])
        if created:
            user.set_password('1234')
            user.email = f"{info['username']}@test.com"
            user.save()

        person, _ = Person.objects.get_or_create(user=user)
        person.role = info['role']
        person.nameStaff = info['staff']
        person.save()
        user_objs[info['staff']] = person

    # 2. רשימת משימות מורחבת (יוזרק מחדש בכל הרצה)
    tasks_data = [
        # משימות Frontend (fr)
        {'name': 'בניית Navbar', 'desc': 'יצירת תפריט ניווט רספונסיבי', 'staff': 'fr', 'status': 'nw', 'exec': None},
        {'name': 'אופטימיזציית תמונות', 'desc': 'שיפור מהירות טעינה בדף הבית', 'staff': 'fr', 'status': 'ip',
         'exec': 'fr'},
        {'name': 'תיקון פונטים', 'desc': 'שינוי פונט המערכת ל-Heebo', 'staff': 'fr', 'status': 'co', 'exec': 'fr'},

        # משימות Backend (ba)
        {'name': 'הגדרת DB', 'desc': 'יצירת טבלאות חדשות למערכת הניהול', 'staff': 'ba', 'status': 'nw', 'exec': None},
        {'name': 'אינטגרציה עם Stripe', 'desc': 'חיבור מערכת תשלומים', 'staff': 'ba', 'status': 'ip', 'exec': 'ba'},
        {'name': 'גיבוי שרת', 'desc': 'הגדרת סקריפט גיבוי יומי', 'staff': 'ba', 'status': 'co', 'exec': 'ba'},

        # משימות UX (ux)
        {'name': 'מחקר משתמשים', 'desc': 'ראיונות עם 5 משתמשי קצה', 'staff': 'ux', 'status': 'nw', 'exec': None},
        {'name': 'Wireframes למובייל', 'desc': 'סקיצות למסכי האפליקציה', 'staff': 'ux', 'status': 'ip', 'exec': 'ux'},

        # משימות QA (qa)
        {'name': 'בדיקת עומסים', 'desc': 'סימולציה של 1000 משתמשים בו-זמנית', 'staff': 'qa', 'status': 'nw',
         'exec': None},
    ]

    for t in tasks_data:
        executor = user_objs.get(t['exec']) if t['exec'] else None

        Task.objects.create(
            name=t['name'],
            description=t['desc'],
            nameStaff=t['staff'],
            end_date=date.today() + timedelta(days=7),
            status=t['status'],
            executor=executor
        )
        print(f"נוצרה משימה: {t['name']}")

    print("\nהסקריפט הסתיים בהצלחה! הנתונים עודכנו.")


if __name__ == '__main__':
    seed()