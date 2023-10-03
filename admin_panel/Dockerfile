FROM python:3.10
COPY . /usr/src/app/admin_panel/
WORKDIR /usr/src/app/admin_panel/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /usr/src/app/admin_panel/requirements.txt
CMD ["python", "start.py"]
