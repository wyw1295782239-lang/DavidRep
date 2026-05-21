from django.contrib.sessions.models import Session
import datetime

# 获取所有未过期的session
sessions = Session.objects.filter(expire_date__gt=datetime.datetime.now())

print(f"Found {sessions.count()} active sessions")

for session in sessions:
    data = session.get_decoded()
    print(f"Session key: {session.session_key}")
    print(f"Session data: {data}")
    print("-" * 50)
