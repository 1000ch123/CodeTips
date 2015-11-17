package main

import (
	"fmt"
)

func fib() func() int {
	val1 := 1
	val2 := 0
	return func() int {
		val1, val2 = val2, val1+val2
		return val2
	}
}

func main() {
	f := fib()
	for i := 0; i < 10; i++ {
		fmt.Println(f())
	}
}
