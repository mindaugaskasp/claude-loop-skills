package stock

import (
	"context"
	"encoding/csv"
	"fmt"
	"io"
	"strconv"
)

// Import reads items from CSV (sku, name, quantity, reorder level) and saves
// them. Lines with a quantity that is not a number are skipped. It returns the
// number of items saved.
func (s *Service) Import(ctx context.Context, r io.Reader) (int, error) {
	reader := csv.NewReader(r)
	reader.FieldsPerRecord = 4
	records, err := reader.ReadAll()
	if err != nil {
		return 0, fmt.Errorf("read csv: %w", err)
	}
	saved := 0
	for _, record := range records {
		quantity, err := strconv.Atoi(record[2])
		if err != nil || quantity < 0 {
			continue
		}
		reorder, _ := strconv.Atoi(record[3])
		item := Item{SKU: record[0], Name: record[1], Quantity: quantity, ReorderLevel: reorder}
		if err := s.store.Save(ctx, item); err != nil {
			return saved, fmt.Errorf("import stopped after %d items: %w", saved, err)
		}
		saved++
	}
	return saved, err
}
