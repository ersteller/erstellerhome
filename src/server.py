# server function load website 

# maybe render markdown as html sites
# 
# 
from flask import Flask, Response
import urllib.request # for forwarding requests

import markdown
import os

archivepath = "/app/archive/"
# archivepath = "/archive"

htmlwrapper = """<!DOCTYPE html> <html> <head><meta charset="utf-8"><link href="/styles/default.css" type="text/css" rel="stylesheet" /><link href="/styles/markdown1.css" type="text/css" rel="stylesheet" /><title>{titel}</title></head><body>{body}</body></html>"""
foldertplt = """<h1>Folder listing of {folder}</h1><ul>{items}</ul>"""
imagetplt = """<img src="{src}">"""
videotplt = """<video> <source src="{src}"/> </video>"""

md = markdown.Markdown(extensions = [
                  'codehilite',
                  'meta'
                ], 
                output_format="html5")

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/home')
def home():
    with open('site/index.html') as f:
        return f.read()

@app.route('/img/archive/<path:arg>')
def imgarchive (arg):
    print("img archive: ",arg)
    try:
        with open(archivepath + '/' + arg, 'rb') as f:
            return f.read()
    except Exception as e:
        return e

imgextlist = ['.jpg', '.png', '.gif', '.jpeg', '.bmp']
vidextlist  = ['.mp4', '.webm', '.ogg', '.avi', '.mov'] 

@app.route('/archive/', defaults={'arg':'.'})
@app.route('/archive/<path:arg>')
def archive (arg):
    print("archive arg: ",arg)
    # /srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archiv/backup1/
    # --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive
    # archive/5.jpg
    path = archivepath + '/' + arg
    base, extension = os.path.splitext(arg)
    lext = extension.lower()
    if lext in imgextlist:
        titel = arg
        path = '/img/archive/'+ arg     # we need to have a url to the src of the binary image file that is diffrent from the html file
        imageelement = imagetplt.format(src=path)
        out =  htmlwrapper.format(body=imageelement, titel=titel)
    elif lext in vidextlist: # we need some player
        titel = arg
        path = '/img/archive/'+ arg     # we need to have a url to the src of the binary video file that is diffrent from the html file
        videoelement = videotplt.format(src=path)
        out =  htmlwrapper.format(body=videoelement, titel=titel)
    else: # list folder
        folder = arg
        try:
            items = []
            for f in os.listdir(path):
                items.append('<li><a href="/archive/{folder}/{file}">{file}</a></li>'.format(folder=folder,file=f))
            items.sort(key=lambda e: e.lower()) # todo dont mix files and folders
            body = foldertplt.format(folder=folder, items="\n".join(items))
            out = htmlwrapper.format(title="Folder "+folder, body=body)
        except Exception as e:
            return e
    return out

@app.route('/site/<arg>')
def site (arg):
    print("site arg: ",arg)
    try:
        with open('site/'+arg+'.html') as f:
            return f.read()
    except Exception as e:
        return e

@app.route('/forward/<arg>')
def forward (arg):
    print("forward arg: ", arg)
    try:
        # get file from url and return it
        s = urllib.request.urlopen(arg).read().decode()
        return s
    except Exception as e:
        return e
    
@app.route('/styles/<arg>')
def styles (arg):
    print("styles arg: ",arg)
    try:
        with open('styles/'+arg) as f:
            css = f.read()
            return Response(css, mimetype='text/css')
    except Exception as e:
        return e

@app.route('/img/<arg>')
def img (arg):
    print("img arg: ",arg)
    try:
        with open('img/'+arg,'rb') as f:
            return f.read()
    except Exception as e:
        return e

@app.route('/favicon.ico')
def fav ():
    try:
        with open('img/ersteller.png','rb') as f:
            return f.read()
    except Exception as e:
        return e

@app.route('/api/pull') 
def pull(): 
    print("git pull")
    res = os.system("git pull")
    status = 200 if res == 0 else res
    return Response("pulled", status=status)

@app.route('/api/conv') 
def reconv(): 
    print("conv",)
    files = ['site/'+f for f in os.listdir('site') if os.path.isfile('site/'+f) and '.md' in f] # get .md files
    print(files)
    conv(files)
    return Response("converted", status=200)

def conv(files):
    # open files to be converted
    # open new file and fill it with html and save 
    # maybe make routs to converted sites
    for fpath in files: 
        with open(fpath, 'r') as f:
            text = f.read()
        html = md.convert(text)
        md_meta =  md.Meta
        metatitle = md_meta.get('title')[0] # [0] -> converts one element list to string
        outhtml = htmlwrapper.format(titel=metatitle, body=html)

        htmlpath = fpath.rsplit('.',1)[0] + ".html"
        with open(htmlpath, 'w') as f:
            f.write(outhtml)
        md.reset()

if __name__ == '__main__':
  conv(["site/index.md",
        "site/links.md",
        "site/locals.md",
        "site/forward.md",
            ])
  #app.run(host='0.0.0.0', port=8000, debug=True ) for local debugging
  app.run(host='0.0.0.0', port=80)


