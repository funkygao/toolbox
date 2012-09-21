/**
 * 检查每个人曾经提交过的文件的数量，排序输出
 */
package main

import (
    "fmt"
    "os/exec"
    "log"
    "strconv"
    "strings"
)

/**
 * 获取某个用户的提交过的文件数量
 */
func filesOfUser(username string) int {
    git := fmt.Sprintf("git log --author=%s --pretty=%%H | while read commit_hash; do git show --oneline --name-only $commit_hash | tail -n+2; done | sort | uniq | wc -l", username)
    out, err := exec.Command("sh", "-c", git).Output()
    if err != nil {
        log.Fatal(err)
    }

    println(username + " ...")

    count := fmt.Sprintf("%s", out)
    count = strings.TrimSpace(count)
    n, err := strconv.Atoi(count)
    if err != nil {
        log.Fatal(err)
    }

    return n
}

/**
 * 找出所有VCS用户名
 */
func getUsers() []string {
    git := "git log --pretty=format:%an | sort | uniq"
    out, err := exec.Command("sh", "-c", git).Output()
    if err != nil {
        log.Fatal(err)
    }

    o := fmt.Sprintf("%s\n", out)
    return strings.Split(o, "\n")
}

/**
 * 总排行
 */
func topUsers() map[string] int {
    users := make(map[string] int)
    usernames := getUsers()
    fmt.Println(usernames)
    for _, name := range usernames {
        if len(strings.TrimSpace(name)) > 0 && !strings.Contains(name, " ") {
            users[name] = filesOfUser(name)
        }
    }

    return users
}

func main() {
    getUsers()
    result := topUsers()
    for k, v := range result {
        fmt.Printf("%15s\t%d\n", k, v)
    }
}

