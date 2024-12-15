FROM ainatarun/flaskbase:latest

COPY requirements.txt requirements.txt

RUN \
 pip install --no-cache-dir -r requirements.txt && \
 apk --purge del .build-deps

COPY . /calendly/
WORKDIR /calendly

COPY entrypoint.sh /usr/bin/
ENTRYPOINT ["bash", "entrypoint.sh"]
