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

docker run -d -p 80:80 --name erstellerhome --restart unless-stopped erstellerhome python /app/src/server.py

### rebuild and deploy
docker build -t erstellerhome . && docker stop erstellerhome && docker rm erstellerhome && docker run -d --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 --name erstellerhome --restart unless-stopped erstellerhome python /app/src/server.py

### with archive
docker run -d --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 --name erstellerhome --restart unless-stopped erstellerhome python /app/src/server.py

# for debugging
## in production
docker run -dt --rm --mount  type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 --name erstellerhome erstellerhome bash
## in test
docker run -dt --rm --mount  type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 8888:80 --name erstellerhometest erstellerhome bash

-v $HOME/.ssh/:/home/builduser/.ssh/:ro

# TODO:
- implement forwarding or status 
- maybe think about css for markdown output  [style](https://github.com/jasonm23/markdown-css-themes/blob/gh-pages/markdown1.css) [default](https://raw.githubusercontent.com/richleland/pygments-css/master/default.css)
- https
- maybe add check for Doorbird to be online (try to push notification to phone (reqires https)). 
- add shader integration

## https 
ssl cert  
301 redirect 
check all links are with https  

```
# https://certbot.eff.org/instructions?ws=other&os=snap
sudo snap install --classic certbot  
sudo ln -s /snap/bin/certbot /usr/bin/certbot  
# either or of the following   
sudo certbot certonly --standalone      # spin up temporary webserver for cert gen  
sudo certbot certonly --webroot         # webserver needs to serve files from /.well-known/acme-challenge
# for renewal testing 
sudo certbot renew --dry-run
```
