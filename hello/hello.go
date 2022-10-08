package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("Hello, go")
	fmt.Println("Cpu cnt : ", runtime.NumCPU())
}
