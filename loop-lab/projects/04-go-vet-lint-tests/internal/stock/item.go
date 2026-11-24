// Package stock holds the stock-keeping rules of the warehouse.
package stock

import "errors"

// Errors returned by the service.
var (
	ErrNotFound        = errors.New("item not found")
	ErrInsufficient    = errors.New("not enough stock")
	ErrInvalidQuantity = errors.New("quantity must be greater than zero")
)

// Item is one kind of thing kept in the warehouse.
type Item struct {
	SKU          string `json:"sku"`
	Name         string `json:"name"`
	Quantity     int    `json:"quantity"`
	ReorderLevel int    `json:"reorder_level"`
}

// Low reports whether the item is at or below its reorder level.
func (i Item) Low() bool {
	return i.Quantity <= i.ReorderLevel
}
