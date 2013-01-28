%{
int wordcount=0;
%}
chars [A-Za-z\_\'\.\"]
numbers ([0-9])+
delim [" "\n\t]
whitespace {delim}+
words {chars}+
%%
{words} {wordcount++;}
{whitespace} {}
{numbers} {}
%%
int main()
{
    yylex(); /* start the analysis */
    printf(" No of words: %d\n", wordcount);
}

int yywrap()
{
    return 1;
}

