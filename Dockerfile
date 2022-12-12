FROM python:3.10-alpine

WORKDIR /app

ENV PARSE_TIMETABLE=0
ENV PARSE_GROUPS=0
ENV INIT_TIMETABLE=0

COPY requirements.txt requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


COPY . .

COPY start.sh .

RUN chmod +x ./start.sh

CMD [ "./start.sh" ]