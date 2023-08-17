# server function load website 

# maybe render markdown as html sites
# 
# 

from flask import Flask
from markdown import markdown

app = Flask(__name__)

@app.route('/')
def home():
  return "hello world!"

@app.route('/site/*')
def site (arg):
    try:
       with open(arg) as f:
          return f.read()
    except Exception as e:
       return e.message 

def conv(files):
    # open files to be converted
    # open new file and fill it with html and save 
    # maybe make routs to converted sites
    for fpath in files: 
      with open(fpath, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
      htmlpath = fpath.rsplit('.',1)[0] + ".html"
      with open(htmlpath, 'w') as f:
        f.write(html)

if __name__ == '__main__':
  conv(["site/index.md",
            "site/links.md"
            ])
  app.run(host='0.0.0.0', port=80)


