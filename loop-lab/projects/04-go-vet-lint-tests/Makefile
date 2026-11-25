BIN := bin/warehouse

.PHONY: build vet lint test check

build:
	go build -o $(BIN) ./cmd/server

vet:
	go vet ./...

lint:
	golangci-lint run

test:
	go test -race ./...

check: vet lint test
