// reddit CLI
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type Item struct {
	Title, Url string
    Comment int `json:"num_comments"`
}

func (this Item) String() string {
    return fmt.Sprintf("%s (%d comments)\n\t%s\n", this.Url, this.Comment, this.Title)
}

type Response struct {
	Data struct {
		Children []struct {
			Data Item
		}
	}
}

func main() {
    var query = "golang"
    if len(os.Args) == 2 {
        query = os.Args[1]
    }
    url := fmt.Sprintf("http://www.reddit.com/r/%s.json", query)
	resp, e := http.Get(url)
	if e != nil {
		panic(e)
	}
    defer resp.Body.Close()

	r := new(Response)
	json.NewDecoder(resp.Body).Decode(r)
	for _, d := range r.Data.Children {
		fmt.Println(d.Data)
	}
    println("Total", len(r.Data.Children))
}
