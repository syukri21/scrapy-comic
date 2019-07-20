def write_data(files):
    with open("scraping/output.py", "wb+")as f:
        f.write('data = {}'.format(files).encode())


def write_old(files):
    with open("scraping/olddata.py", "wb+")as f:
        f.write('old = {}'.format(files).encode())


def write_images(files):
    with open("scraping/tmpimages.py", "wb+")as f:
        f.write('images = {}'.format(files).encode())


def write_update(files):
    with open("scraping/update.py", "wb+")as f:
        f.write('update = {}'.format(files).encode())
