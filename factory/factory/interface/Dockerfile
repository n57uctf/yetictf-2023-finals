FROM golang:1.20.3

WORKDIR /tmp/interface

COPY . .

ENV CGO_ENABLED=1

RUN go build -o ./out/main .

EXPOSE 8181/tcp

CMD ["/tmp/interface/out/main"]

