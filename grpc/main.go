package main

import (
	"gprc2/protobuf"
	"log"
)

func main() {
	log.Println("start!")
	req := protobuf.HelloRequest{}
	if req.Name != "" {
		log.Println("error!")
	} else {
		log.Println("success!")
	}
}
