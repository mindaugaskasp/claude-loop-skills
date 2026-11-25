package stock

import (
	"context"
	"errors"
	"strings"
	"testing"
)

func newTestService(t *testing.T) *Service {
	t.Helper()
	store := NewMemoryStore()
	err := store.Save(context.Background(), Item{SKU: "BOLT-8", Name: "Bolt M8", Quantity: 10, ReorderLevel: 4})
	if err != nil {
		t.Fatalf("seed store: %v", err)
	}
	return NewService(store)
}

func TestReceiveAddsToStock(t *testing.T) {
	svc := newTestService(t)
	item, err := svc.Receive(context.Background(), "BOLT-8", 5)
	if err != nil {
		t.Fatalf("Receive: %v", err)
	}
	if item.Quantity != 15 {
		t.Errorf("quantity = %d, want 15", item.Quantity)
	}
}

func TestShip(t *testing.T) {
	tests := []struct {
		name     string
		sku      string
		quantity int
		want     int
		wantErr  error
	}{
		{name: "takes from stock", sku: "BOLT-8", quantity: 3, want: 7},
		{name: "everything", sku: "BOLT-8", quantity: 10, want: 0},
		{name: "more than there is", sku: "BOLT-8", quantity: 11, wantErr: ErrInsufficient},
		{name: "zero", sku: "BOLT-8", quantity: 0, wantErr: ErrInvalidQuantity},
		{name: "unknown item", sku: "NUT-8", quantity: 1, wantErr: ErrNotFound},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			svc := newTestService(t)
			item, err := svc.Ship(context.Background(), tt.sku, tt.quantity)
			if !errors.Is(err, tt.wantErr) {
				t.Fatalf("error = %v, want %v", err, tt.wantErr)
			}
			if err == nil && item.Quantity != tt.want {
				t.Errorf("quantity = %d, want %d", item.Quantity, tt.want)
			}
		})
	}
}

func TestLowStock(t *testing.T) {
	svc := newTestService(t)
	ctx := context.Background()
	if _, err := svc.Ship(ctx, "BOLT-8", 6); err != nil {
		t.Fatalf("Ship: %v", err)
	}
	low, err := svc.LowStock(ctx)
	if err != nil {
		t.Fatalf("LowStock: %v", err)
	}
	if len(low) != 1 || low[0].SKU != "BOLT-8" {
		t.Errorf("low stock = %+v, want only BOLT-8", low)
	}
}

func TestImportSkipsBadQuantities(t *testing.T) {
	svc := newTestService(t)
	data := "NUT-8,Nut M8,40,10\nWASHER-8,Washer M8,many,10\nSCREW-4,Screw 4x30,25,5\n"
	saved, err := svc.Import(context.Background(), strings.NewReader(data))
	if err != nil {
		t.Fatalf("Import: %v", err)
	}
	if saved != 2 {
		t.Errorf("saved = %d, want 2", saved)
	}
}
