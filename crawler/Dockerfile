FROM python:3.8.10

RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN apt-get install -y libglib2.0
RUN apt --fix-broken install

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

RUN mkdir -p /build
WORKDIR /build
COPY . /build
# Install chrome stable
RUN wget https://www.slimjetbrowser.com/chrome/files/104.0.5112.102/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

CMD ["scrapyd"]