FROM work:0.2
WORKDIR /tmp/docker
COPY requirements.txt /tmp/docker/

# ---------------Start of requirements block ---------------
RUN pip install --default-timeout=100 -r /tmp/docker/requirements.txt
# ---------------End of requirements block -----------------

