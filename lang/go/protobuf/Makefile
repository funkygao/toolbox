all:gen main.go
	go run main.go

gen:
	mkdir -p demo
	protoc --go_out=./demo demo.proto

