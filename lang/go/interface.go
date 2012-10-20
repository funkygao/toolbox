package main

func main() {
    var a interface{} = "asdf"
    println(a.(string))
}
