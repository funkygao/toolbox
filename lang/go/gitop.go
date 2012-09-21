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
    "sort"
    "runtime"
    "flag"
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
 * 找出所有git用户名
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
 *
 * concurrent 并发数
 */
func topUsers(concurrent int) map[string] int {
    runtime.GOMAXPROCS(concurrent + 5)

    println("concurrent:", concurrent)
    printSeperator(50, "=")

    //c := make(chan map[string] int, concurrent)

    users := make(map[string] int)
    usernames := getUsers()
    fmt.Println("users:", usernames)
    printSeperator(50, "-")
    for _, name := range usernames {
        if len(strings.TrimSpace(name)) > 0 && !strings.Contains(name, " ") {
            users[name] = filesOfUser(name)
        }
    }

    return users
}

func printSeperator(num int, content string) {
    for i := 0; i < num; i++ {
        print(content)
    }
    println()
}

type ValSorter struct {
    Keys []string
    Values []int
}

func newValSorter(m map[string] int) *ValSorter {
    vs := &ValSorter{
        Keys: make([]string, len(m)),
        Values: make([]int, len(m)),
    }

    for k, v := range m {
        vs.Keys = append(vs.Keys, k)
        vs.Values = append(vs.Values, v)
    }

    return vs
}

func (vs *ValSorter) Sort() {
    sort.Sort(vs)
}

func (vs *ValSorter) Len() int {
    return len(vs.Values)
}

func (vs *ValSorter) Less(i, j int) bool {
    return vs.Values[i] < vs.Values[j]
}

func (vs *ValSorter) Swap(i, j int) {
    vs.Values[i], vs.Values[j] = vs.Values[j], vs.Values[i]
    vs.Keys[i], vs.Keys[j] = vs.Keys[j], vs.Keys[i]
}

func main() {
    const COUNT_THRESHOLD = 5

    var concurrent = flag.Int("c", 1, "concurrent")
    flag.Parse()

    result := topUsers(*concurrent)
    // 对结果进行排序
    vs := newValSorter(result)
    vs.Sort()

    printSeperator(50, "=")
    // 输出排序后的结果
    for _, name := range vs.Keys {
        count := result[name]
        if count > COUNT_THRESHOLD {
            fmt.Printf("%15s\t%d\n", name, count)
        }
    }
}

