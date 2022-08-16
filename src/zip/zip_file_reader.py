import zipfile


def zipfile_reader(zip_filename: str, filename: str = ''):
    with zipfile.ZipFile(zip_filename) as z:
        if not filename:
            filename = z.filelist[0].filename
        with z.open(filename, 'r') as f:
            for line in f:
                yield line
