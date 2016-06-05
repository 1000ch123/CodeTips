package main

import (
	"encoding/json"
	"fmt"
	"github.com/syndtr/goleveldb/leveldb"
)

type Message struct {
	Id   int
	Body string
}

func main() {
	// connection
	db, err := leveldb.OpenFile("./level", nil)
	if err != nil {
		return
	}
	defer db.Close()

	for i := 0; i < 10; i++ {
		// data
		m := &Message{i, "message"}
		json_data, err := json.Marshal(m)
		if err != nil {
			return
		}

		// insert
		key := fmt.Sprintf("message:%d", i)
		err = db.Put([]byte(key), json_data, nil)
		if err != nil {
			return
		}
	}

	iter := db.NewIterator(nil, nil)
	for iter.Next() {
		key := iter.Key()
		value := iter.Value()
		fmt.Printf("%v: %v\n", string(key), string(value))
	}
	iter.Release()
	err = iter.Error()
}
