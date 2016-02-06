// Copyright © 2016 Alan A. A. Donovan & Brian W. Kernighan.
// License: https://creativecommons.org/licenses/by-nc-sa/4.0/

package intset

import "fmt"

func Example_one() {
	//!+main
	var x, y IntSet
	x.Add(1)
	x.Add(144)
	x.Add(9)
	fmt.Println(x.String()) // "{1 9 144}"

	y.Add(9)
	y.Add(42)
	fmt.Println(y.String()) // "{9 42}"

	x.UnionWith(&y)
	fmt.Println(x.String()) // "{1 9 42 144}"

	fmt.Println(x.Has(9), x.Has(123)) // "true false"
	//!-main

	// Output:
	// {1 9 144}
	// {9 42}
	// {1 9 42 144}
	// true false
}

func Example_two() {
	var x IntSet
	x.Add(1)
	x.Add(144)
	x.Add(9)
	x.Add(42)

	//!+note
	fmt.Println(&x)         // "{1 9 42 144}"
	fmt.Println(x.String()) // "{1 9 42 144}"
	fmt.Println(x)          // "{[4398046511618 0 65536]}"
	//!-note

	// Output:
	// {1 9 42 144}
	// {1 9 42 144}
	// {[4398046511618 0 65536]}
}

func Example_ex1() {
	var x IntSet
	x.Add(1)
	x.Add(144)
	x.Add(9)
	x.Add(42)

	fmt.Println(x.Len()) // 4

	x.Remove(42)
	fmt.Println(&x) // "{1 9 144}"

	x.Clear()
	fmt.Println(&x) // "{}"

	y := x.Copy()
	x.Add(1)
	fmt.Println(&x) // "{1}"
	fmt.Println(y)  // "{}"

	// Output:
	// 4
	// {1 9 144}
	// {}
	// {1}
	// {}
}

func Example_ex2() {
	var x IntSet
	x.AddAll(1, 9, 144)

	fmt.Println(&x) // "{1 9, 144}"

	// Output:
	// {1 9 144}
}

func Example_ex3_1() {
	var x, y IntSet
	x.AddAll(1, 9, 144)
	y.AddAll(1, 9, 16)

	x.IntersectWith(&y)
	fmt.Println(&x) // "{1 9}"

	// Output:
	// {1 9}
}

func Example_ex3_2() {
	var x, y IntSet
	x.AddAll(1, 9, 144)
	y.AddAll(1, 9, 16)

	x.DifferenceWith(&y)
	fmt.Println(&x) // "{144}"

	// Output:
	// {144}
}

func Example_ex3_3() {
	var x, y IntSet
	x.AddAll(1, 9, 144)
	y.AddAll(1, 9, 16)

	x.SymmetricDiffernceWith(&y)
	fmt.Println(&x) // "{16 144}"

	// Output:
	// {16 144}
}

func Example_ex3_4() {
	var x IntSet
	x.AddAll(1, 9, 144)

	for _, v := range x.Elems() {
		fmt.Println(v)
	}

	// Output:
	// 1
	// 9
	// 14
}
