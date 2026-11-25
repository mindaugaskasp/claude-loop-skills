# frozen_string_literal: true

module Seedbox
  # The library's rules.
  module Policy
    LOAN_DAYS = 180
    MAX_OPEN_LOANS = 4
    REMIND_DAYS_BEFORE = 14

    def self.due_on(lent_on)
      lent_on + LOAN_DAYS
    end

    def self.may_borrow?(open_loans)
      open_loans < MAX_OPEN_LOANS
    end

    def self.remind?(due_on, today)
      (due_on - today).to_i <= REMIND_DAYS_BEFORE
    end
  end
end
