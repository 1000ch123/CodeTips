package main

import (
	"fmt"
)

func main() {
	// 3.1
	x, y, z := 0x08, 0xff, 0x11
	fmt.Printf("%08b\n", x)
	fmt.Printf("%08b\n", y)
	fmt.Printf("%08b\n", z)

	f := 1e100
	i := int(f)
	fmt.Println(f)
	fmt.Println(i)

	// 3.2
	var a float64
	fmt.Println(a, -a, 1/a, -1/a, a/a)

	var b int32 = 1
	var c int
	c = int(b)
	fmt.Println(c)
}
