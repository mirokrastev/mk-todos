import os


def delete_image(path):
    if not os.path.exists(path):
        return
    os.remove(path)


def upload_new_picture(profile, new_picture):
    old_picture = profile.avatar.name.split('/')[-1]
    if old_picture != 'default-user-avatar.jpg':
        delete_image(profile.avatar.path)
    profile.avatar = new_picture
