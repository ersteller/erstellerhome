# server function load website 

# maybe render markdown as html sites
# 
# 
from flask import Flask, Response
import markdown
import os

head =  """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <link href="/styles/default.css" type="text/css" rel="stylesheet" />
    <link href="/styles/markdown1.css" type="text/css" rel="stylesheet" />
    <title>%(title)s</title>
  </head> 

<body>
"""
outtail = """

</body>

</html>
"""

md = markdown.Markdown(extensions = [
                  'codehilite',
                  'meta'
                ], 
                output_format="html5")

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def home():
  with open('site/index.html') as f:
    return f.read()

@app.route('/site/<arg>')
def site (arg):
    print("site arg: ",arg)
    try:
       with open('site/'+arg+'.html') as f:
          return f.read()
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
      outhead = head % { 'title' : metatitle }

      htmlpath = fpath.rsplit('.',1)[0] + ".html"
      with open(htmlpath, 'w') as f:
        f.write(outhead + html + outtail)
      md.reset()

if __name__ == '__main__':
  conv(["site/index.md",
            "site/links.md"
            ])
  #app.run(host='0.0.0.0', port=8000, debug=True ) for local debugging
  app.run(host='0.0.0.0', port=80)


