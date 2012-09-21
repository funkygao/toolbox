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

func filesOfUser(username string) int {
    git := fmt.Sprintf("git log --author=%s --pretty=%%H | while read commit_hash; do git show --oneline --name-only $commit_hash | tail -n+2; done | sort | uniq | wc -l", username)
    out, err := exec.Command("sh", "-c", git).Output()
    if err != nil {
        log.Fatal(err)
    }

    count := fmt.Sprintf("%s", out)
    count = strings.TrimSpace(count)
    i, e := strconv.Atoi(count)
    if e != nil {
        log.Fatal(e)
    }

    return i
}

func topUsers() map[string] int {
    users := make(map[string] int)
    usernames := []string{"gaopeng", "ouyangde"}
    for _, name := range usernames {
        users[name] = filesOfUser(name)
    }

    return users
}

func main() {
    result := topUsers()
    for k, v := range result {
        fmt.Printf("%15s\t%d\n", k, v)
    }
}

