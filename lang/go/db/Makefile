C=100
L=1000

all:go insert

insert:go
	@echo "C:$C L:$L"
	./bench -op insert -c $C -l $L

update:go
	@echo "C:$C L:$L"
	./bench -op update -c $C -l $L

clean:go
	./bench -op delete


go:mysql.go
	@go build
