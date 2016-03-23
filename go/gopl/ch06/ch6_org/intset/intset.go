// Copyright © 2016 Alan A. A. Donovan & Brian W. Kernighan.
// License: https://creativecommons.org/licenses/by-nc-sa/4.0/

// See page 165.

// Package intset provides a set of integers based on a bit vector.
package intset

import (
	"bytes"
	"fmt"
)

//!+intset

// An IntSet is a set of small non-negative integers.
// Its zero value represents the empty set.
type IntSet struct {
	words []uint
}

const bitsize = 32 << (^uint(0) >> 63)

// Has reports whether the set contains the non-negative value x.
func (s *IntSet) Has(x int) bool {
	word, bit := x/bitsize, uint(x%bitsize)
	return word < len(s.words) && s.words[word]&(1<<bit) != 0
}

func (s *IntSet) Len() (cnt int) {
	for _, word := range s.words {
		for word > 0 {
			if word%2 == 1 {
				cnt++
			}
			word = word / 2
		}
	}
	return
}

// Add adds the non-negative value x to the set.
func (s *IntSet) Add(x int) {
	word, bit := x/bitsize, uint(x%bitsize)
	for word >= len(s.words) {
		s.words = append(s.words, 0)
	}
	s.words[word] |= 1 << bit
}

func (s *IntSet) AddAll(xs ...int) {
	for _, x := range xs {
		s.Add(x)
	}
}

func (s *IntSet) Remove(x int) {
	if !s.Has(x) {
		return
	}

	word, bit := x/bitsize, uint(x%bitsize)
	s.words[word] ^= 1 << bit

	return
}

func (s *IntSet) Clear() {
	s.words = []uint{0}
	return
}

func (s *IntSet) Copy() *IntSet {
	words := make([]uint, s.Len())
	copy(words, s.words)
	t := IntSet{words}
	return &t
}

// UnionWith sets s to the union of s and t.
func (s *IntSet) UnionWith(t *IntSet) {
	for i, tword := range t.words {
		if i < len(s.words) {
			s.words[i] |= tword
		} else {
			s.words = append(s.words, tword)
		}
	}
}

func (s *IntSet) IntersectWith(t *IntSet) {
	for i, _ := range s.words {
		if i < len(t.words) {
			s.words[i] &= t.words[i]
		} else {
			s.words[i] = 0
		}
	}
}

func (s *IntSet) DifferenceWith(t *IntSet) {
	for i, _ := range s.words {
		if i < len(t.words) {
			s.words[i] &^= t.words[i]
		}
	}
}

func (s *IntSet) SymmetricDiffernceWith(t *IntSet) {
	for i, _ := range t.words {
		s.words[i] ^= t.words[i]
	}
}

func (s *IntSet) Elems() (vs []int) {
	for i, word := range s.words {
		cnt := 0
		for word > 0 {
			if word%2 == 1 {
				vs = append(vs, cnt+bitsize*i)
			}
			word = word / 2
			cnt++
		}
	}
	return
}

//!-intset

//!+string

// String returns the set as a string of the form "{1 2 3}".
func (s *IntSet) String() string {
	var buf bytes.Buffer
	buf.WriteByte('{')
	for i, word := range s.words {
		if word == 0 {
			continue
		}
		for j := 0; j < bitsize; j++ {
			if word&(1<<uint(j)) != 0 {
				if buf.Len() > len("{") {
					buf.WriteByte(' ')
				}
				fmt.Fprintf(&buf, "%d", bitsize*i+j)
			}
		}
	}
	buf.WriteByte('}')
	return buf.String()
}

//!-string
