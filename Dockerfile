#
FROM python:3.10

#
WORKDIR /code

#
COPY ./req.txt /code/req.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/req.txt

#
COPY ./ /code

#
EXPOSE 9001

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9001"]