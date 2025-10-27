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

docker stop erstellerhome ; docker rm erstellerhome

### rebuild and deploy
docker build -t erstellerhome . && docker stop erstellerhome && docker rm erstellerhome && docker run -d -v $HOME/.ssh/:/home/builduser/.ssh/:ro --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 --name erstellerhome --restart unless-stopped erstellerhome python /app/src/server.py

### with archive
docker run -d --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 --name erstellerhome --restart unless-stopped erstellerhome python /app/src/server.py

# for debugging
## in production
docker run -dt --rm --mount  type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 --name erstellerhome erstellerhome bash
## in test
docker run -dt --rm -v $HOME/.ssh/:/home/builduser/.ssh/:ro --mount  type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 8888:80 --name erstellerhometest erstellerhome bash
docker stop erstellerhometest; docker rm erstellerhometest

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

# prod
docker run -d -v $HOME/.ssh/:/root/.ssh/:ro --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 -p 443:443 --name ucfehome --restart unless-stopped ucfehome
# debug
docker run -it -v $HOME/.ssh/:/root/.ssh/:ro --mount type=bind,src=/srv/dev-disk-by-uuid-1e0dd676-fe98-461e-b8ba-9f7a6607af4d/public/erotic/archive,dst=/app/archive -p 80:80 -p 443:443 -v ${PWD}:/app -p 8000:8000 --name ucfehome --rm ucfehome bash

# for https we should use nginx
https://nginx.org/en/linux_packages.html#Ubuntu

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


# caddy problems 

```
open /root/.local/share/caddy/acme/acme-v02.api.letsencrypt.org-directory/users/default/default.json: no such file or directory"

2025/10/27 19:54:25.319 INFO    trying to solve challenge       {"identifier": "ersteller.net", "challenge_type": "tls-alpn-01", "ca": "https://acme-staging-v02.api.letsencrypt.org/directory"}
2025/10/27 19:54:26.275 ERROR   challenge failed        {"identifier": "ersteller.net", "challenge_type": "tls-alpn-01", "problem": {"type": "urn:ietf:params:acme:error:connection", "title": "", "detail": "77.179.227.37: Connection refused", "instance": "", "subproblems": null}}
github.com/mholt/acmez/v3.(*Client).pollAuthorization
        github.com/mholt/acmez/v3@v3.1.2/client.go:557
github.com/mholt/acmez/v3.(*Client).solveChallenges
025/10/27 19:54:26.276 ERROR   validating authorization        {"identifier": "ersteller.net", "problem": {"type": "urn:ietf:params:acme:error:connection", "title": "", "detail": "77.179.227.37: Connection refused", "instance": "", "subproblems": null}, "order": "https://acme-staging-v02.api.letsencrypt.org/acme/order/238158373/28274043243", "attempt": 2, "max_attempts": 3}
2025/10/27 19:54:26.276 ERROR   tls.obtain      could not get certificate from issuer   {"identifier": "ersteller.net", "issuer": "acme-v02.api.letsencrypt.org-directory", "error": "HTTP 400 urn:ietf:params:acme:error:connection - 77.179.227.37: Connection refused"}
2025/10/27 19:54:26.276 ERROR   tls.obtain      will retry      {"error": "[ersteller.net] Obtain: [ersteller.net] solving challenge: ersteller.net: [ersteller.net] authorization failed: HTTP 400 urn:ietf:params:acme:error:connection - 77.179.227.37: Connection refused (ca=https://acme-staging-v02.api.letsencrypt.org/directory)", "attempt": 2, "retrying_in": 120, "elapsed": 68.947623296, "max_duration": 2592000}
2025/10/27 19:56:26.275 INFO    tls.obtain      obtaining certificate   {"identifier": "ersteller.net"}
```
