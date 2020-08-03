FROM fedora

RUN dnf update -y && \
    dnf install python -y 

COPY ./requirements.txt /opt/requirements.txt

RUN python -m pip install -r /opt/requirements.txt

VOLUME [ "/exec" ]
WORKDIR /exec
ENTRYPOINT [ "bash" ]