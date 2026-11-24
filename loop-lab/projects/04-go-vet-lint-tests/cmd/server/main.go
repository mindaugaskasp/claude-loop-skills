// Command server runs the warehouse HTTP service.
package main

import (
	"flag"
	"log"
	"net/http"
	"time"

	"example.com/warehouse/internal/httpapi"
	"example.com/warehouse/internal/stock"
)

func main() {
	addr := flag.String("addr", ":8080", "address to listen on")
	flag.Parse()

	svc := stock.NewService(stock.NewMemoryStore())
	server := &http.Server{
		Addr:              *addr,
		Handler:           httpapi.New(svc),
		ReadHeaderTimeout: 5 * time.Second,
	}
	log.Printf("warehouse listening on %s", *addr)
	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}
