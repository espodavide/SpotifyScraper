
FROM selenium/standalone-chrome:112.0-chromedriver-112.0 

RUN sudo apt-get update && sudo apt-get install -y python3-pip

WORKDIR /SpotifyScraper

COPY . ./

RUN sudo pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080 443

CMD ["sudo","/usr/bin/python3", "app_running.py"]
