package test
 
import (
    "fmt"
	"labix.org/v2/mgo"
	"labix.org/v2/mgo/bson"
	"testing"
)
 
const INSERT_COUNT int = 10000
 
type User struct {
	Id    bson.ObjectId `bson:"_id,omitempty" json:"_id"`
	Email string        `bson:"email" json:"email"`
}
 
func (self *User) Init() {
	self.Id = bson.NewObjectId()
}
 
func BenchmarkFlatInsert(b *testing.B) {
	b.StopTimer()
	// Database
	dbs, err := mgo.Dial("mongodb://localhost/ac-bench")
	if err != nil {
		panic(err)
	}
 
	// Collections
	uc := dbs.Clone().DB("").C("users")
	defer dbs.Clone().DB("").Session.Close()
 
	// Clear DB
	uc.RemoveAll(bson.M{})
	b.StartTimer()
 
	for n := 0; n < b.N; n++ {
 
		count := INSERT_COUNT
		for i := 0; i < count; i++ {
			loop_user := User{}
			loop_user.Init()
			loop_user.Email = fmt.Sprintf("report-%d@example.com", i)
			if err := uc.Insert(&loop_user); err != nil {
				panic(err)
			}
		}
 
	}
}
 
func BenchmarkParallelInsert(b *testing.B) {
	b.StopTimer()
	// Database
	dbs, err := mgo.Dial("mongodb://localhost/ac-bench")
	if err != nil {
		panic(err)
	}
 
	// Collections
	uc := dbs.Clone().DB("").C("users")
	defer dbs.Clone().DB("").Session.Close()
 
	// Clear DB
	uc.RemoveAll(bson.M{})
	b.StartTimer()
 
	for n := 0; n < b.N; n++ {
 
		count := INSERT_COUNT
		sem := make(chan bool, count)
		for i := 0; i < count; i++ {
			go func(i int) {
				loop_user := User{}
				loop_user.Init()
				loop_user.Email = fmt.Sprintf("report-%d@example.com", i)
				if err := uc.Insert(&loop_user); err != nil {
					panic(err)
				}
				sem <- true
			}(i)
		}
		for j := 0; j < count; j++ {
			<-sem
		}
 
	}
}
 
func BenchmarkBatchInsert(b *testing.B) {
	b.StopTimer()
	// Database
	dbs, err := mgo.Dial("mongodb://localhost/ac-bench")
	if err != nil {
		panic(err)
	}
 
	// Collections
	uc := dbs.Clone().DB("").C("users")
	defer dbs.Clone().DB("").Session.Close()
 
	// Clear DB
	uc.RemoveAll(bson.M{})
	b.StartTimer()
 
	for n := 0; n < b.N; n++ {
 
		count := INSERT_COUNT
		users := make([]User, count)
		for i := 0; i < count; i++ {
			loop_user := User{}
			loop_user.Init()
			loop_user.Email = fmt.Sprintf("report-%d@example.com", i)
			users[i] = loop_user
		}
		if err := uc.Insert(&users); err != nil {
			panic(err)
		}
 
	}
}
