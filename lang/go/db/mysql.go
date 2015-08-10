package main

import (
	"database/sql"
	"flag"
	"fmt"
	"sync"
	"time"

	"github.com/funkygao/golib/color"
	_ "github.com/funkygao/mysql"
)

var opts struct {
	concurrent int
	loop       int
	op         string
}

func dieIfErr(err error) {
	if err != nil {
		panic(err)
	}
}

var idgen chan int

const dsn = "dbtest:dbtest@tcp(10.77.145.36:3306)/dbtest?charset=utf8"

//const dsn = "test:test@tcp(10.77.145.28:10066)/TESTDB?charset=utf8"

func init() {
	flag.IntVar(&opts.concurrent, "c", 100, "concurrent mysql conns")
	flag.IntVar(&opts.loop, "l", 10000, "each mysql conn exec how many times")
	flag.StringVar(&opts.op, "op", "insert", "<insert|update|delete>")
	flag.Parse()
}

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

	var rows int
	switch opts.op {
	case "insert":
		for i := 0; i < opts.concurrent; i++ {
			wg.Add(1)
			go func(seq int) {
				insert(seq, opts.loop)
				wg.Done()
			}(i)
		}
		rows = opts.loop * opts.concurrent

	case "update":
		for i := 0; i < opts.concurrent; i++ {
			wg.Add(1)
			go func(seq int) {
				update(seq, opts.loop)
				wg.Done()
			}(i)
		}
		rows = opts.loop * opts.concurrent

	case "delete":
		db, err := sql.Open("mysql", dsn)
		dieIfErr(err)
		rs, err := db.Exec("DELETE FROM user")
		if err != nil {
			fmt.Println(err)
		} else {
			if n, err := rs.RowsAffected(); err != nil {
				fmt.Println(err)
			} else {
				fmt.Printf("%d rows deleted\n", n)
				rows = int(n)
			}
		}
		db.Close()

	default:
		fmt.Println("unknown operation:", opts.op)
	}

	wg.Wait()
	elapsed := time.Since(t0)
	dur := int(elapsed.Seconds())
	if dur == 0 {
		dur = 1
	}
	fmt.Printf("%s elapsed:%s, rows:%d %s:%d\n", opts.op, elapsed, rows,
		color.Red("qps"),
		rows/dur)

}

func insert(seq int, loops int) {
	db, err := sql.Open("mysql", dsn)
	dieIfErr(err)
	defer db.Close()

	for i := 0; i < loops; i++ {
		uid := <-idgen
		query := "INSERT INTO user(uid, name, age) values(?,?,?)"
		if _, err := db.Exec(query, uid, "foo", 20); err != nil {
			fmt.Println(err)
			return
		}
	}

}

func update(seq int, loops int) {
	db, err := sql.Open("mysql", dsn)
	dieIfErr(err)
	defer db.Close()

	for i := 0; i < loops; i++ {
		uid := <-idgen
		query := "UPDATE user SET name=? WHERE uid=?"
		if _, err := db.Exec(query, "bar", uid); err != nil {
			fmt.Println(err)
			return
		}
	}

}
