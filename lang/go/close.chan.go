// Shows even when you close a chan, reeiver still got the buffered contents
package main

import "fmt"

func main() {
    ch := make(chan bool, 2)
    ch <- true
    ch <- true
    // Once a channel has been closed, you cannot send a value on this channel, but 
    // you can still receive from the channel.
    close(ch)

    for i := 0; i < cap(ch) +1 ; i++ {
        v, ok := <- ch
        fmt.Println(v, ok)
    }
}
