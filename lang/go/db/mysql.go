package main

import (
	"database/sql"
	"fmt"
	"os"
	"sync"
	"time"

	_ "github.com/funkygao/mysql"
)

func dieIfErr(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	var wg sync.WaitGroup
	t0 := time.Now()
	if os.Args[1] == "insert" {
		for i := 0; i < 1000; i++ {
			wg.Add(1)
			go func(seq int) {
				insert(seq, 10000)
				wg.Done()
			}(i)
		}

	} else {
		for i := 0; i < 1000; i++ {
			wg.Add(1)
			go func(seq int) {
				update(seq, 10000)
				wg.Done()
			}(i)
		}
	}

	wg.Wait()
	fmt.Println(time.Since(t0))

}

func insert(seq int, loops int) {
	db, err := sql.Open("mysql", "dbtest:dbtest@tcp(10.77.145.36:3306)/dbtest?charset=utf8")
	dieIfErr(err)

	for i := 0; i < loops; i++ {
		uid := seq*100000 + i
		query := "INSERT INTO user(uid, name, age) values(?,?,?)"
		db.Exec(query, uid, "foo", 20)
	}

}

func update(seq int, loops int) {
	db, err := sql.Open("mysql", "dbtest:dbtest@tcp(10.77.145.36:3306)/dbtest?charset=utf8")
	dieIfErr(err)

	for i := 0; i < loops; i++ {
		uid := seq*100000 + i
		query := "UPDATE user SET name=? WHERE uid=?"
		db.Exec(query, "bar", uid, "foo")
	}

}
