package main

import (
	"fmt"
	"regexp"
)

// embed regexp.Regexp in a new type so we can extend it
type myRegexp struct {
	*regexp.Regexp
}

// add a new method to our new regular expression type
func (r *myRegexp) FindStringSubmatchMap(s string) map[string]string {
	captures := make(map[string]string)

	match := r.FindStringSubmatch(s)
	if match == nil {
		return captures
	}

	for i, name := range r.SubexpNames() {
		// Ignore the whole regexp match and unnamed groups
		if i == 0 || name == "" {
			continue
		}

		captures[name] = match[i]

	}
	return captures
}

// an example regular expression
var myExp = myRegexp{regexp.MustCompile(`(?P<first>\d+)\.(\d+).(?P<second>\d+)`)}

func main() {
	fmt.Printf("%#v", myExp.FindStringSubmatchMap("1234.5678.9"))

	re := regexp.MustCompilePOSIX("a*")
	fmt.Println(re.MatchString("dabcdd"))
}
