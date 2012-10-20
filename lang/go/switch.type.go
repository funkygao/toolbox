package main

func main() {
    typeCheck(4, "saf", true)
}

func typeCheck(p ...interface{}) {
    for _, v := range p {
        switch v.(type) {
        case int:
            println(v, "int")
        case string:
            println(v, "string")
        case bool:
            println(v, "bool")
        }
    }
}

