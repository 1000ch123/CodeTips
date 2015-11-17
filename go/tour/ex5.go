package main

import (
	"fmt"
	"math/cmplx"
)

func Cbrt(x complex128) complex128 {
	z := 1.0 + 0i
	for cmplx.Abs(cmplx.Pow(z, 3)-x) > 0.00001 {
		z = z - (z*z*z-x)/(3*z*z)
	}
	return z
}

func main() {
	fmt.Println(cmplx.Pow(2, 3))
	fmt.Println(Cbrt(2))
}
