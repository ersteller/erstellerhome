# erstellerhome

docker container for hosting website

git clone git@github.com:ersteller/erstellerhome.git
or 
git pull 

docker build -t erstellerhome .
docker run -it -p 80:80 erstellerhome bash
docker run -it -p 80:80 erstellerhome python /app/src/server.py

docker run erstellerhome -d --restart-always -p 80:80