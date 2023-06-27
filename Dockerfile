FROM python:3.10
COPY ./ /usr/app/src
WORKDIR /usr/app/src
ENV PYTHONPATH /usr/app/src
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
CMD ["python", "./admin_panel/admin.py"]