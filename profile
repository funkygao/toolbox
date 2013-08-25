# to start mysql on startup
# sudo port load mysql5-server

. /opt/local/etc/profile.d/bash_completion.sh
. /opt/local/share/doc/task/scripts/bash/task_completion.sh
. /opt/local/etc/bash_completion.d/git-completion.bash

alias vbox='VBoxManage startvm openstack1 --type gui'
alias ubuntu='VBoxManage startvm ubuntu --type gui'
alias win7='VBoxManage startvm win7 --type gui'
alias openstack='ssh openstack@172.16.0.1'
alias linux='ssh gp@172.16.0.2'
alias xen='ssh gp@172.16.0.3'

alias goc='go build -gcflags "-N -l"'
alias vt='cd /Users/apple/src/code.google.com/p/vitess/go'
alias gobench='go test -v -test.bench=".*"'
alias dbsql='vi ~/kx/docs/db.sql'
alias dbpsql='vi /Users/apple/kx/src/platform/platform/doc/platform_db.sql'
alias portupdate='sudo port -d selfupdate'
alias locateupdate='sudo /usr/libexec/locate.updatedb'
alias lockme='/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend'
alias pdb='python -m pdb'
alias share='python -m SimpleHTTPServer'
alias duh='du -s ./* | sort -n | cut -f 2- | xargs du -sh'

funcs()
{
    local cur
    cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=(`global -c $cur`)
}
complete -F funcs global

function vc() {
    vi `locate "$1" | \grep -w "$1" | \grep php | \grep 'kx/src/' | \grep -v _utf8 | \grep -v orig | \grep -v svn | \grep -v doc`
}

alias gl='global -x'
alias jps='jps -l | sort'

alias t='task'

alias dl='cd ~/github/dlogmon'
alias to='cd ~/github/toolbox/lang/go'
alias dll='cd ~/github/dlogmon/src/kx/dlog'
alias wee='cd /Users/apple/github/weedfs/weed-fs/src/'
alias tb='cd ~/github/toolbox/lang/go'
alias g='cd ~/github'
alias kx='cd ~/kx/src/'
alias kxp='cd ~/kx/src/platform'
alias kxa='cd ~/kx/src/apps'
alias kxb='cd ~/kx/src/base/www/'
alias kxh='cd ~/kx/src/base/www/include/http'

alias godocserver='godoc -http=":9000"'
alias doc='godoc'
alias bench='go test -test.bench=".*"'
alias gdc='godoc . | less'

alias phpdump='php -dextension=pod.so'
alias httpwatch='sudo tcpick -i en1 -C -a -t -v -yP -T1 "port 80"'
alias pi='phing'
alias phpunit='phpunit --colors'
alias pu='phpunit --colors --coverage-html report'
alias puw='phpunit --colors'
alias pul='phpunit --colors --testdox'

alias fd='find . -name '
alias grep='grep --color -n'
alias pi='phing'
alias tu='top -o cpu' # cpu
alias tm='top -o vsize' # memory
alias db='mysql -u root -h localhost demos'
alias tcpstat='sudo tcpstat -i en1'
alias ldd='otool -L'
alias bsh='java bsh.Console'
alias hfs='hadoop fs'
alias me='cd ~/github/WebMe/webme/'
alias vp='source ~/vpython/bin/activate'
alias wgetr='wget -l1 --random-wait -r -p -e robots=off -U chrome'
alias httphead='curl -v -s -o /dev/null '
alias eman='erl -man'
alias phpunit='phpunit --colors'

alias github='git push origin master'

alias m='mvn –o package –Dmaven.test.skip=true'
alias mysite='cd /Users/apple/vir_python/projects/MySite/mysite'
alias strace='dtruss'

alias vmstat='vm_stat'
alias less='less -r'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias ls='ls -lh'
alias lsa='ls -ah'
alias lst='ls -ltr'
alias lss='ls -Sr'
alias df='df -h'
alias lynx='w3m'
alias ll='ls -aF'
alias dir='ls -F|grep /'
alias lf='ls -F|grep -v /'
alias ml='tail -f /var/log/mail.log'

alias a='cd /Library/WebServer/Documents/'
alias ws='cd ~/devs/java/workspace'
alias d='cd ~/devs/'
alias j='cd ~/devs/java'
alias p='cd ~/devs/python'
alias oil='cd /Users/apple/github//oil/oil'

alias myadmin='mysql -u root'

alias mongocli='mongo localhost:12987'
alias mongoadmin='w3m http://localhost:13987/'
alias mongostat='mongostat -h localhost:12987 5'

alias gvim='/Applications/MacVim.app/Contents/MacOS/Vim -g'

export EDITOR='vi'
export SVN_EDITOR=vim
export JAVA_HOME=/Library/Java/Home
export GRADLE_HOME=/opt/app/gradle-1.3/
export SCALA_HOME=/opt/local

export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

#export DYLD_LIBRARY_PATH=/usr/local/lib:/opt/local/lib:/opt/app/spread/lib:/usr/local/mysql/lib:$DYLD_LIBRARY_PATH

export HADOOP_HOME=/opt/app/hadoop
export PIG_CLASSPATH=$HADOOP_HOME/conf

export PATH=/opt/app/gdb/bin:$PATH:/opt/local/share/java/android-sdk-mac_x86/tools/:/opt/app/sysbench/bin:/usr/local/mysql/bin:/opt/local/bin:/opt/local/sbin:/opt/app/nmap/bin:/opt/app/hadoop/bin:/opt/app/innotop:/opt/app/protobuf/bin:/opt/app/tcpstat/bin:/opt/local/Library/Frameworks/Python.framework/Versions/2.6/bin/:/opt/local/share/java/android-sdk-mac_x86/platform-tools:/opt/app/jython2.5.2:/opt/app/pear/bin/:~/scripts/:/opt/app/gperftools/bin/:$GRADLE_HOME/bin

export MANPATH=$MANPATH:/opt/app/siege/man:/opt/app/tcpstat/man:/opt/app/gperftools/share/man
#export GOBIN=/usr/local/go/bin
export GOROOT=/usr/local/go
export GOPATH=~/github/dlogmon
export MAVEN_OPTS='-Xms128m -Xmx512m'
export M2_REPO='/Users/apple/.m2/repository'

RED="\033[33;31m"
GREEN="\033[33;32m"
YELLOW="\033[33;33m"
BLUE="\033[33;34m"
PURPLE="\033[33;35m"
RESET="\033[m"

function parse_git_branch {
    git_branch=$(git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/')
    git_branch="${GREEN}${git_branch}${RESET}";
    echo -e $git_branch
}

export PS1="\[\e[33;1m\][\u@\h \w\$(parse_git_branch)]$\e[m\]"

#export PS1='[\u:\w@\h]$'
#export PS1="\[\e[33;1m\][\$(date +%H:%M) \u@\h \w]$\[\e[m\]"
#export PS1='\[\e[33;1m\][\u@\h \w\[\033[32m\]$(__git_ps1 "(%s)")\033[m]$\[\033[00m\]'

#export PYTHONPATH=$PYTHONPATH:/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages
export PYTHONSTARTUP=~/.pythonstartup
