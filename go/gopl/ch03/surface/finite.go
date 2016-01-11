package main

import (
	"fmt"
	"math"
)

func main() {
	a := 0.0
	fmt.Println(math.IsInf(1/a, 1))

	if true && true {
		fmt.Println(true)
	}
}
