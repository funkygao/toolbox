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

var idgen chan int

const dsn = "dbtest:dbtest@tcp(10.77.145.36:3306)/dbtest?charset=utf8"

func main() {
	var wg sync.WaitGroup
	t0 := time.Now()
	idgen = make(chan int, 1000)
	go func() {
		id := 0
		for {
			id++
			idgen <- id
		}
	}()
	const C = 500
	const Loop = 10000

	if os.Args[1] == "insert" {
		for i := 0; i < C; i++ {
			wg.Add(1)
			go func(seq int) {
				insert(seq, Loop)
				wg.Done()
			}(i)
		}

	} else {
		for i := 0; i < C; i++ {
			wg.Add(1)
			go func(seq int) {
				update(seq, Loop)
				wg.Done()
			}(i)
		}
	}

	wg.Wait()
	elapsed := time.Since(t0)
	fmt.Printf("elapsed: %s, qps: %d\n", elapsed, Loop*C/int(elapsed.Seconds()))

}

func insert(seq int, loops int) {
	db, err := sql.Open("mysql", dsn)
	dieIfErr(err)
	defer db.Close()

	for i := 0; i < loops; i++ {
		uid := <-idgen
		query := "INSERT INTO user(uid, name, age) values(?,?,?)"
		db.Exec(query, uid, "foo", 20)
	}

}

func update(seq int, loops int) {
	db, err := sql.Open("mysql", dsn)
	dieIfErr(err)
	defer db.Close()

	for i := 0; i < loops; i++ {
		uid := <-idgen
		query := "UPDATE user SET name=? WHERE uid=?"
		db.Exec(query, "bar", uid)
	}

}
