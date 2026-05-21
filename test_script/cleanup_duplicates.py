import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from user.models import UserInfo
from django.db.models import Count, Min

# Find duplicate usernames
duplicates = UserInfo.objects.values('username').annotate(
    count=Count('id'),
    min_id=Min('id')
).filter(count__gt=1)

print('Duplicate usernames found:', list(duplicates))

# Delete duplicates, keeping the one with the lowest ID
for dup in duplicates:
    username = dup['username']
    min_id = dup['min_id']
    
    # Delete all except the one with min_id
    deleted = UserInfo.objects.filter(
        username=username
    ).exclude(
        id=min_id
    ).delete()
    
    print(f'Deleted {deleted[0]} duplicates for username: {username}')

print('Cleanup completed!')