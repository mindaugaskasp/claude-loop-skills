package stock

import (
	"context"
	"sort"
	"sync"
)

// Store keeps items.
type Store interface {
	Get(ctx context.Context, sku string) (Item, error)
	Save(ctx context.Context, item Item) error
	List(ctx context.Context) ([]Item, error)
}

// MemoryStore is a Store that keeps everything in memory.
type MemoryStore struct {
	mu    sync.RWMutex
	items map[string]Item
}

// NewMemoryStore returns an empty MemoryStore.
func NewMemoryStore() *MemoryStore {
	return &MemoryStore{items: make(map[string]Item)}
}

// Get returns the item with the given SKU or ErrNotFound.
func (m *MemoryStore) Get(ctx context.Context, sku string) (Item, error) {
	if err := ctx.Err(); err != nil {
		return Item{}, err
	}
	m.mu.RLock()
	defer m.mu.RUnlock()
	item, ok := m.items[sku]
	if !ok {
		return Item{}, ErrNotFound
	}
	return item, nil
}

// Save stores the item, replacing any item with the same SKU.
func (m *MemoryStore) Save(ctx context.Context, item Item) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	m.mu.Lock()
	defer m.mu.Unlock()
	m.items[item.SKU] = item
	return nil
}

// List returns all items ordered by SKU.
func (m *MemoryStore) List(ctx context.Context) ([]Item, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	m.mu.RLock()
	defer m.mu.RUnlock()
	out := make([]Item, 0, len(m.items))
	for _, item := range m.items {
		out = append(out, item)
	}
	sort.Slice(out, func(a, b int) bool { return out[a].SKU < out[b].SKU })
	return out, nil
}
