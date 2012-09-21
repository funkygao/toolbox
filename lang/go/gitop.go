/**
 * 检查每个人曾经提交过的文件的数量，排序输出
 */
package main

import (
    "fmt"
    "os/exec"
    "os"
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

    count := fmt.Sprintf("%s", out)
    count = strings.TrimSpace(count)
    n, err := strconv.Atoi(count)
    if err != nil {
        log.Fatal(err)
    }

    return n
}

func filesOfUsers(users []string, c chan map[string] int) {
    for _, name := range users {
        count := filesOfUser(name)
        msg := map[string] int{name: count}
        c <- msg
    }
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

    outStr := fmt.Sprintf("%s", out)
    outStr = strings.TrimSpace(outStr)

    userArr := strings.Split(outStr, "\n")
    return userArr
}

/**
 * 总排行
 *
 * concurrent 并发数
 */
func topUsers(concurrent int) map[string] int {
    runtime.GOMAXPROCS(concurrent + 5)

    println("concurrent =", concurrent)
    printSeperator(50, "=")

    usernames := getUsers()
    chunkSize := len(usernames) / concurrent
    fmt.Println("count =", len(usernames))
    fmt.Println("chunkSize =", chunkSize)
    fmt.Println("users =", usernames)
    printSeperator(50, "-")

    // 创建总人数长度的channel
    channels := make(chan map[string] int, len(usernames))

    usercount, seqInChunk, chunk := 0, 0, 0
    names := make([]string, 0)
    for index, name := range usernames {
        if isUsernameValid(name) {
            usercount ++ // 有效用户总数
            seqInChunk ++ // 本次chunk内该用户名的序列号
            names = append(names, name) // 本chunk内的用户名列表
            if seqInChunk >= chunkSize {
                printNamesInChunk(chunk, names)

                go filesOfUsers(names, channels)

                seqInChunk = 0
                chunk ++
                names = make([]string, 0)
            } else if (chunk == concurrent && index == len(usernames) -1) {
                // 最后的chunk，its item num < chunkSize
                printNamesInChunk(chunk, names)

                go filesOfUsers(names, channels)
            }
        } else {
            println("Invalid name:", name)
            println()
        }
    }

    // 收集各个goroutines的放入channel的结果
    r := make(map[string] int) // result
    for i := 0; i < usercount; i++ {
        chunkResult := <- channels
        fmt.Println("<-msg:", chunkResult)
        for k, v := range chunkResult {
            r[k] = v
        }
    }

    return r
}

func printNamesInChunk(chunk int, names []string) {
    fmt.Print("chunk: ", chunk, " count: ", len(names), " users: [")
    for i, name := range(names) {
        print(i, ":", name, ", ")
    }
    println("]\n")
}

func isUsernameValid(name string) bool {
    trimmedName := strings.TrimSpace(name)
    return len(trimmedName) > 1 && !strings.Contains(trimmedName, "no author")
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

    os.Exit(0)
}

