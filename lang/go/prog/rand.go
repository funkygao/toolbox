package main

import (
    "crypto/rand"
    "encoding/base64"
    "fmt"
)

func create_random_id(bytes int) string {
    random_bytes := make([]byte, bytes)
    random_id := make([]byte, base64.URLEncoding.EncodedLen(bytes))
    rand.Read(random_bytes)
    base64.URLEncoding.Encode(random_id, random_bytes)
    return string(random_id)
}

// 创建指定长度的随机字符串
func main() {
    fmt.Println(create_random_id(20))
}
