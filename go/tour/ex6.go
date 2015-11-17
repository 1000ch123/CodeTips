package main

import (
	"fmt"
	"math"
)

// float値を扱う新しい型をつくる
type ErrNegativeSqrt float64

// 上記の型にError メソッドを実装することで，error interfaceを充足する
func (e ErrNegativeSqrt) Error() string {
	return fmt.Sprintf("cannot Sqrt negative number %v", float64(e))
}

// 返り値は常に
// (正常値:nil) もしくは (異常値, エラー) となるぽさがある
// 型型している
// type Result (float64, error) みたいのしたさがあるが type がよくわからんちん
func Sqrt(x float64) (float64, error) {
	if x < 0 {
		return x, ErrNegativeSqrt(x)
	}
	z := 1.0
	for math.Abs(z*z-x) > 0.00001 {
		z = z - (z*z-x)/(2*z)
	}
	return z, nil
}

func main() {
	fmt.Println(Sqrt(2))
	fmt.Println(Sqrt(-2))
}
