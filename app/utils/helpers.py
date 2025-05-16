ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_extension(mimetype):
    if not mimetype.startswith('image/'):
        return None

    ext = mimetype.split('/')[-1].lower()
    if ext == 'jpeg':
        return 'jpg'
    elif ext in ['png', 'gif', 'jpg']:
        return ext
    else:
        return None
