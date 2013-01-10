#!/usr/bin/env bash
#=================================================================
#
# 在通过gerrit/git进行开发前，需要运行本脚本，设置git相关的参数
#
#=================================================================

# 可以配置的参数
#--------------
gerritPort=29418
gerritHost='192.168.0.142'
gerritRepo='base.git'

echo "==========================================================="
echo "  You MUST run this script at root dir of this repository  "
echo 
echo "  i,e ./scripts/setup-for-gerrit.sh"
echo "==========================================================="
echo
echo "press ENTER to continue, ^C to abort"
read

# 设置git的用户名user.name和电子邮件user.email
#---------------------------------------------
setup_git_user() {
  read -ep "Please enter your full name, e.g. 'gaopeng': " name
  git config user.name "$name"
  read -ep "Please enter your email address, e.g. 'gaopeng@corp.kaixin001.com': " email
  git config user.email "$email"
}

# 引导用户设置user.name和user.email
#----------------------------------
for (( ; ; ))
do
  # 显示当前设置的值
  gitName=$(git config user.name)
  gitEmail=$(git config user.email)
  echo -e "\nYour commits will have the following author information:

    $gitName <$gitEmail>
"
  # 让用户确认，如果不正确，那就再次设置
  read -ep "Is the name and email address above correct? [y/N] " correct
  if [ "$correct" != "y" ] && [ "$correct" != "Y" ]; then
    setup_git_user
  else
    break
  fi
done

# 设置 gerrit remote: review
#---------------------------
gerrit_user() {
  read -ep "Enter your gerrit user (Gerrit Settings/Profile) [$USER]: " gu
  if [ "$gu" == "" ]; then
    gu=$USER
  fi
  echo -e "\nConfiguring 'review' remote with user '$gu'..."
  url=ssh://$gu@$gerritHost:$gerritPort/$gerritRepo
  if git config remote.review.url >/dev/null; then
    # Correct the remote url
    git remote set-url review $url  || \
      die "Could not set review remote."
  else
    # Add a new one
    git remote add review $url || \
      die "Could not add review remote."
  fi
  cat << EOF

For more information on working with Gerrit,

    http://192.168.0.201:8080/pages/viewpage.action?pageId=754060   
EOF
}

# 引导用户设置review remote并安装commit-msg hook
#-----------------------------------------------
for (( ; ; ))
do
  echo -e "\nThe configured Gerrit remote URL is:"
  echo
  git config remote.review.url
  gu=`git config remote.review.url | sed -e 's/^ssh:\/\///' | sed -e  's/@'$gerritHost:$gerritPort'\/'$gerritRepo'//'`
  echo
  read -ep "Is the username and URL correct? [y/N]: " correct
  if [ "$correct" != "y" ] && [ "$correct" != "Y" ]; then
    gerrit_user
  else
    scp -P $gerritPort -p $gu@$gerritHost:/hooks/commit-msg .git/hooks/
    break
  fi
done

cat << EOF

********************************************************************************
    Congratulations! 

    Gerrit is ready for you!!
********************************************************************************
Git aliases installed
--------------------------------
  prepush          - view a short form of the commits about to be pushed,
                     relative to origin/master
  syncmaster       - on any local branch, run it to pull from gerrit master to local master
  squash           - combine all prepush commits into one commit for review.
  review-push      - push the current topic branch to Gerrit for code review.
  noreview-push    - push the current topic branch to Gerrit for code share.

Kaixin git workflow
--------------------------------
  $ git checkout -b feature_branch
  ...work and commit
  $ git rebase master
  $ git prepush
  $ git squash
  $ git review-push
  ...logon gerrit web to invite reviewers
  ...wait for good news
  $ git checkout master
  $ git branch -d feature_branch
  $ git pull
  $ git checkout -b another_feature_branch

EOF

# 设置git别名
#-----------
git_prepushnum="\$(git log --pretty=oneline origin/master.. | wc -l | sed -e 's/^[ \t]*//')"
git config alias.prepush 'log --graph --stat origin/master..'
git config alias.squash "!sh -c \"git rebase -i HEAD~${git_prepushnum}\""
git config alias.syncmaster 'pull -v origin master:master'
git_branch="\$(git symbolic-ref HEAD | sed -e 's|^refs/heads/||' | sed -e 's/sandbox\///')"
git config alias.review-push "!sh -c \"git push review HEAD:refs/for/master/${git_branch}\""
git config alias.noreview-push "!sh -c \"git push origin HEAD:refs/heads/sandbox/${git_branch}\""

# 设置git color
#--------------
git config color.diff "auto"
git config color.branch "auto"
git config color.interactive "auto"
git config color.grep "auto"
