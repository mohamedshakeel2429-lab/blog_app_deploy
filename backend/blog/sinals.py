from django.contrib.auth.models import Group,Permission

def create_groups_permissions(sender, **kwargs):
    
    try:
          readers_group,created = Group.objects.get_or_create(name = 'readers')
          author_group,created = Group.objects.get_or_create(name = 'authors')
          editor_group,created = Group.objects.get_or_create(name = 'editors')
          
          # Defining permissions for authors
          
          readers_permissions = [
              Permission.objects.get(codename='view_post'),]
          author_permissions = [
              Permission.objects.get(codename='add_post'),
              Permission.objects.get(codename='change_post'),
              Permission.objects.get(codename='view_post'),
              Permission.objects.get(codename='delete_post'),
          ]
          publish_post,created = Permission.objects.get_or_create(codename='can_publish_post',name='Can Publish Post',content_type_id=7)
          editor_permissions = [
              publish_post,                    
              Permission.objects.get(codename='add_post'),
              Permission.objects.get(codename='change_post'),
              Permission.objects.get(codename='delete_post'),
              Permission.objects.get(codename='view_post'),
          ]
          # Assigning permissions to groups
          readers_group.permissions.set(readers_permissions)
          author_group.permissions.set(author_permissions)    
          editor_group.permissions.set(editor_permissions)
          print("Groups and permissions created successfully.")
    except Exception as e:
        print(f"Error creating groups and permissions: {e}")
    
        