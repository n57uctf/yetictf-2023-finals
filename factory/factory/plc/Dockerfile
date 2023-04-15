FROM alpine:3.17.3
ENV addr="0.0.0.0:502"
WORKDIR /app
COPY . /app/
EXPOSE 502/tcp
RUN chmod +x /app/plc
ENTRYPOINT /app/plc
