# erstellerhome
This is a small webserver. It converts Markdown files to html files.  
URLs are relative to root without html file extension.


## build
docker container for hosting website

git clone git@github.com:ersteller/erstellerhome.git  
or 
git pull  

docker build -t erstellerhome .  
docker run -it -p 80:80   erstellerhome bash  
docker run -it -p 80:80  erstellerhome python /app/src/server.py  

docker push 

docker run erstellerhome -d --restart-always -p 80:80  

# TODO:
add pull command url  
add convert command url  
maybe think about css for markdown output  
