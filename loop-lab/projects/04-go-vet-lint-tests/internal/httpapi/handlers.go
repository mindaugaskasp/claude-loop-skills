// Package httpapi exposes the stock service over HTTP.
package httpapi

import (
	"encoding/json"
	"errors"
	"net/http"

	"example.com/warehouse/internal/stock"
)

// API holds the HTTP handlers.
type API struct {
	svc *stock.Service
}

// New returns the handler for the whole API.
func New(svc *stock.Service) http.Handler {
	api := &API{svc: svc}
	mux := http.NewServeMux()
	mux.HandleFunc("GET /items/{sku}", api.getItem)
	mux.HandleFunc("POST /items/{sku}/receive", api.receive)
	mux.HandleFunc("POST /items/{sku}/ship", api.ship)
	mux.HandleFunc("GET /low-stock", api.lowStock)
	mux.HandleFunc("POST /import", api.importCSV)
	return mux
}

type quantityRequest struct {
	Quantity int `json:"quantity"`
}

func (a *API) getItem(w http.ResponseWriter, r *http.Request) {
	item, err := a.svc.Item(r.Context(), r.PathValue("sku"))
	if err != nil {
		writeError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, item)
}

func (a *API) receive(w http.ResponseWriter, r *http.Request) {
	var req quantityRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "body is not valid JSON"})
		return
	}
	item, err := a.svc.Receive(r.Context(), r.PathValue("sku"), req.Quantity)
	if err != nil {
		writeError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, item)
}

func (a *API) ship(w http.ResponseWriter, r *http.Request) {
	var req quantityRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "body is not valid JSON"})
		return
	}
	item, err := a.svc.Ship(r.Context(), r.PathValue("sku"), req.Quantity)
	if err != nil {
		writeError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, item)
}

func (a *API) lowStock(w http.ResponseWriter, r *http.Request) {
	items, err := a.svc.LowStock(r.Context())
	if err != nil {
		writeError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

func (a *API) importCSV(w http.ResponseWriter, r *http.Request) {
	saved, err := a.svc.Import(r.Context(), r.Body)
	if err != nil {
		writeError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, map[string]int{"saved": saved})
}

func writeError(w http.ResponseWriter, err error) {
	status := http.StatusInternalServerError
	switch {
	case errors.Is(err, stock.ErrNotFound):
		status = http.StatusNotFound
	case errors.Is(err, stock.ErrInsufficient):
		status = http.StatusConflict
	case errors.Is(err, stock.ErrInvalidQuantity):
		status = http.StatusBadRequest
	}
	writeJSON(w, status, map[string]string{"error": err.Error()})
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(body)
}
