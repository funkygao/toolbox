============================
setup vim for go programming
============================

Setup
=====

::

    export GOBIN=/usr/local/go/bin

    sudo go get -u github.com/nsf/gocode (-u flag for "update")

    cd /usr/local/go/misc/vim; read readme.txt and install it

    cd; git://github.com/nsf/gocode.git
    cd gocode/vim && ./update.bash

    edit ~/.vimrc and add the following
    imap <C-j> <C-x><C-o>

Usage
=====

In insert mode, type Ctrl-j and use arrow key to navigate the autocomplete choice list

