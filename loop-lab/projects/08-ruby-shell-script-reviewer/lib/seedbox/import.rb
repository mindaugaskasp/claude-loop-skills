# frozen_string_literal: true

module Seedbox
  # Reads the member list exported by the sign-up form.
  class Import
    def initialize(store: Store.new)
      @store = store
    end

    def members(path)
      unless File.exist?(path)
        raise Error, "#{path} does not exist. Give the path to the CSV file the sign-up form exported."
      end

      known = @store.members
      ids = known.map(&:id)
      added = 0

      CSV.foreach(path, headers: true) do |row|
        id = row["member_id"]
        next if id.nil? || ids.include?(id)

        # The form puts the e-mail address in the last column.
        known << Member.new(id: id, name: row["full_name"], email: row[3])
        ids << id
        added += 1
      end

      @store.save_members(known)
      added
    end
  end
end
