# frozen_string_literal: true

module Seedbox
  # The one place that asks what time it is. Everything is kept in UTC so
  # that a loan made late in the evening does not land on the wrong day.
  module Clock
    def self.now
      Time.now.utc
    end

    def self.today
      now.to_date
    end
  end
end
