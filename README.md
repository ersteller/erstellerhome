# erstellerhome
This is a small webserver. It converts Markdown files to html files.  
URLs are relative to root without html file extension.


## build
docker container for hosting website

git clone git@github.com:ersteller/erstellerhome.git  
or 
git pull  

docker build -t erstellerhome .  
docker run -it -p 80:80 erstellerhome bash  
docker run -it -p 80:80 erstellerhome python /app/src/server.py  

docker build -t erstellerhome . && docker run -it -p 80:80  erstellerhome python /app/src/server.py  

docker push 

docker run erstellerhome -d --restart unless-stopped -p 80:80  

docker run -d -p 80:80 -p 443:443 --name erstellerhome --restart unless-stopped erstellerhome

docker stop erstellerhome ; docker rm erstellerhome

### rebuild and deploy
docker build -t erstellerhome . && docker stop erstellerhome && docker run -d -v $HOME/.ssh/:/root/.ssh/:ro --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 -p 443:443 --name erstellerhome --restart unless-stopped erstellerhome

### with archive
# prod
docker run -d -v $HOME/.ssh/:/root/.ssh/:ro --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 -p 443:443 --name erstellerhome --restart unless-stopped erstellerhome
# debug
docker run -it -v $HOME/.ssh/:/root/.ssh/:ro --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 -p 443:443 -v ${PWD}:/app -p 8000:8000 --name erstellerhome --rm erstellerhome bash


# TODO:
- implement forwarding or status 
- maybe think about css for markdown output  [style](https://github.com/jasonm23/markdown-css-themes/blob/gh-pages/markdown1.css) [default](https://raw.githubusercontent.com/richleland/pygments-css/master/default.css)
- maybe add check for Doorbird to be online (try to push notification to phone (reqires https)). 
- add shader integration
