# -*- coding: utf-8 -*-

# -- stdlib --
import json
import os
import shutil
import sys
import urlparse

# -- third party --
from flask import Flask, request, Response
import magic

# -- code --
CONFIG = '/upload/upload.json'
STORE = '/upload/files/store'
TMP = '/upload/files/tmp'
STATE_STORE = '/upload/files/state_store'

app = Flask(__name__)
config = json.loads(open(CONFIG).read())


def resp(v, status=200):
    return Response(json.dumps(v), mimetype='application/json', status=status)


@app.route('/upload', methods=['POST'])
def upload():
    rst = []

    for k, v in request.form.items(multi=True):
        if k == '<ngx_upload_module_dummy>':
            continue

        path, size, sha1, filename = v.split('|', 4)
        size = int(size)
        ext = filename.split('.')[-1].lower()
        sha1fn = '%s.%s' % (sha1, ext)

        def fail(reason):
            os.unlink(path)
            rst.append({
                "name": filename,
                "field_name": k,
                "size": size,
                "error": reason
            })

        if ext not in ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'apng', 'mng'):
            fail('File extension not allowed')
            continue

        mime = magic.from_file(path, mime=True)
        if not mime.startswith('image/'):
            fail('Not an image')
            continue

        size = int(size)
        if size > config['max_size']:
            fail('Size limit exceeded')
            continue

        subdirs = '%s/%s' % (sha1[0:2], sha1[2:4])
        fn = '%s/%s' % (subdirs, sha1fn)

        dest = os.path.join(STORE, fn)
        if not os.path.exists(dest):
            shutil.move(path, dest)
        else:
            os.unlink(path)

        url = urlparse.urljoin(config['prefix'], fn)
        rst.append({
            "name": filename,
            "field_name": k,
            "type": mime,
            "size": size,
            "url": url,
            "thumbnailUrl": url,  # TODO
            "deleteUrl": url,
            "deleteType": "DELETE"
        })

    return resp({"files": rst})


@app.route('/files/<hash1>/<hash2>/<filename>', methods=['DELETE'])
def delete(hash1, hash2, filename):
    if not filename.startswith(hash1 + hash2):
        return resp({'files': []}, 404)

    if not config.get('can_delete', False):
        return resp({'files': []}, 405)

    try:
        os.unlink(os.path.join(STORE, hash1, hash2, filename))
    except:
        pass

    return resp({'files': [{filename: True}]})


def main():
    app.run(host='127.0.0.1', port=int(sys.argv[1]))


def ensure_dirs():
    import pwd
    pw = pwd.getpwnam('www-data')

    for i in xrange(256):
        p = os.path.join(STORE, chr(i).encode('hex'))
        for j in xrange(256):
            p2 = os.path.join(p, chr(j).encode('hex'))
            try:
                os.makedirs(p2)
            except Exception:
                pass

            try:
                os.chown(p2, pw.pw_uid, pw.pw_gid)
            except Exception:
                pass

        try:
            os.chown(p, pw.pw_uid, pw.pw_gid)
        except Exception:
            pass

    for i in [STORE, TMP, STATE_STORE]:
        try:
            os.makedirs(i)
        except:
            pass

        try:
            os.chown(i, pw.pw_uid, pw.pw_gid)
        except Exception:
            pass


if __name__ == '__main__':
    main()
