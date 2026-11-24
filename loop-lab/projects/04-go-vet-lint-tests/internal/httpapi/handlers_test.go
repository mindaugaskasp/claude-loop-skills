package httpapi

import (
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"example.com/warehouse/internal/stock"
)

func newTestAPI(t *testing.T) http.Handler {
	t.Helper()
	store := stock.NewMemoryStore()
	err := store.Save(context.Background(), stock.Item{SKU: "BOLT-8", Name: "Bolt M8", Quantity: 10, ReorderLevel: 4})
	if err != nil {
		t.Fatalf("seed store: %v", err)
	}
	return New(stock.NewService(store))
}

func TestHandlers(t *testing.T) {
	tests := []struct {
		name   string
		method string
		path   string
		body   string
		want   int
	}{
		{name: "get item", method: http.MethodGet, path: "/items/BOLT-8", want: http.StatusOK},
		{name: "get unknown item", method: http.MethodGet, path: "/items/NUT-8", want: http.StatusNotFound},
		{name: "receive", method: http.MethodPost, path: "/items/BOLT-8/receive", body: `{"quantity": 5}`, want: http.StatusOK},
		{name: "ship too many", method: http.MethodPost, path: "/items/BOLT-8/ship", body: `{"quantity": 50}`, want: http.StatusConflict},
		{name: "ship nothing", method: http.MethodPost, path: "/items/BOLT-8/ship", body: `{"quantity": 0}`, want: http.StatusBadRequest},
		{name: "broken body", method: http.MethodPost, path: "/items/BOLT-8/ship", body: `{`, want: http.StatusBadRequest},
		{name: "low stock", method: http.MethodGet, path: "/low-stock", want: http.StatusOK},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			api := newTestAPI(t)
			req := httptest.NewRequest(tt.method, tt.path, strings.NewReader(tt.body))
			rec := httptest.NewRecorder()
			api.ServeHTTP(rec, req)
			if rec.Code != tt.want {
				t.Errorf("status = %d, want %d (body %s)", rec.Code, tt.want, rec.Body.String())
			}
		})
	}
}
