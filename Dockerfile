FROM python:3.8-slim
# Set working directory.
RUN mkdir /app/
WORKDIR /app/

# Copy app files.
COPY . /app/
# Install app dependencies.
RUN pip install -r requirements.txt

# Start pytests
CMD  pytest -v -s --alluredir=/reports operations/test_login.py