# frozen_string_literal: true

module Seedbox
  # Lending, returning and listing loans.
  class Loans
    def initialize(store: Store.new)
      @store = store
    end

    def lend(member_id:, packet_id:)
      loans = @store.loans
      open = loans.count { |l| l.member_id == member_id && l.open? }
      unless Policy.may_borrow?(open)
        raise Error, "Member #{member_id} already has #{open} packets out. One has to come back first."
      end

      today = Clock.today
      loan = Loan.new(
        id: next_id(loans), member_id: member_id, packet_id: packet_id,
        lent_on: today, due_on: Policy.due_on(today), returned_on: nil
      )
      @store.save_loans(loans + [loan])
      loan
    end

    def give_back(loan_id)
      loans = @store.loans
      loan = loans.find { |l| l.id == loan_id }
      raise Error, "There is no loan #{loan_id}. Run 'seedbox due' to see the open loans." if loan.nil?
      raise Error, "Loan #{loan_id} was already returned on #{loan.returned_on}." unless loan.open?

      loan.returned_on = Date.today
      @store.save_loans(loans)
      loan
    end

    def due
      @store.loans.select(&:open?).sort_by(&:due_on)
    end

    private

    # TODO: ids clash if two of us lend at the same moment on two laptops
    def next_id(loans)
      (loans.map { |l| l.id.to_i }.max.to_i + 1).to_s
    end
  end
end
