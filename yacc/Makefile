wc:
	lex wc.lex
	cc -o wc  lex.yy.c

clean:
	rm -f wc
	rm -f lex.yy.c

run:wc
	./wc < lex.yy.c
