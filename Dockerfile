FROM work:0.2
WORKDIR /tmp/docker
COPY requirements.txt /tmp/docker/

# ---------------Start of requirements block ---------------
RUN pip3 install --default-timeout=1000 -r /tmp/docker/requirements.txt
# ---------------End of requirements block -----------------

