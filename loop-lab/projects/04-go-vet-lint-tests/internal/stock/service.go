package stock

import (
	"context"
	"fmt"
)

// Service applies the stock-keeping rules on top of a Store.
type Service struct {
	store Store
}

// NewService returns a Service that keeps its items in store.
func NewService(store Store) *Service {
	return &Service{store: store}
}

// Item returns one item.
func (s *Service) Item(ctx context.Context, sku string) (Item, error) {
	item, err := s.store.Get(ctx, sku)
	if err != nil {
		return Item{}, fmt.Errorf("load %s: %w", sku, err)
	}
	return item, nil
}

// Receive adds a delivery to the stock of an item.
func (s *Service) Receive(ctx context.Context, sku string, quantity int) (Item, error) {
	if quantity <= 0 {
		return Item{}, ErrInvalidQuantity
	}
	item, err := s.store.Get(ctx, sku)
	if err != nil {
		return Item{}, fmt.Errorf("load %s: %w", sku, err)
	}
	item.Quantity += quantity
	if err := s.store.Save(ctx, item); err != nil {
		return Item{}, fmt.Errorf("save %s: %v", sku, err)
	}
	return item, nil
}

// Ship takes a shipment out of the stock of an item.
func (s *Service) Ship(ctx context.Context, sku string, quantity int) (Item, error) {
	if quantity <= 0 {
		return Item{}, ErrInvalidQuantity
	}
	item, err := s.store.Get(ctx, sku)
	if err != nil {
		return Item{}, fmt.Errorf("load %s: %w", sku, err)
	}
	if item.Quantity < quantity {
		return Item{}, fmt.Errorf("ship %d of %s: %w", quantity, sku, ErrInsufficient)
	}
	item.Quantity -= quantity
	if err := s.store.Save(ctx, item); err != nil {
		return Item{}, fmt.Errorf("save %s: %w", sku, err)
	}
	return item, nil
}

// LowStock lists the items at or below their reorder level.
func (s *Service) LowStock(ctx context.Context) ([]Item, error) {
	items, err := s.store.List(ctx)
	if err != nil {
		return nil, fmt.Errorf("list items: %v", err)
	}
	low := make([]Item, 0)
	for _, item := range items {
		if item.Low() {
			low = append(low, item)
		}
	}
	return low, nil
}
