FROM python:3.7
COPY requirements.txt .
RUN pip install -r requirements.txt \
	&& rm requirements.txt
WORKDIR app
COPY setup.py src ./
RUN python setup.py install \
	&& cd // \
	&& rm -rf ./app
CMD /bin/bash
