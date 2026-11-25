# frozen_string_literal: true

module Seedbox
  Loan = Struct.new(:id, :member_id, :packet_id, :lent_on, :due_on, :returned_on, keyword_init: true) do
    def open?
      returned_on.nil?
    end
  end

  Member = Struct.new(:id, :name, :email, keyword_init: true)

  # Reads and writes the CSV files.
  class Store
    LOAN_HEADERS = %w[id member_id packet_id lent_on due_on returned_on].freeze
    MEMBER_HEADERS = %w[id name email].freeze

    def loans
      read(Config.loans_file).map do |row|
        Loan.new(
          id: row["id"],
          member_id: row["member_id"],
          packet_id: row["packet_id"],
          lent_on: Date.iso8601(row["lent_on"]),
          due_on: Date.iso8601(row["due_on"]),
          returned_on: row["returned_on"].to_s.empty? ? nil : Date.iso8601(row["returned_on"])
        )
      end
    end

    def save_loans(loans)
      write(Config.loans_file, LOAN_HEADERS, loans.map { |l| l.to_h.values_at(*LOAN_HEADERS.map(&:to_sym)) })
    end

    def members
      read(Config.members_file).map { |row| Member.new(id: row["id"], name: row["name"], email: row["email"]) }
    end

    def save_members(members)
      write(Config.members_file, MEMBER_HEADERS, members.map { |m| [m.id, m.name, m.email] })
    end

    private

    def read(path)
      return [] unless File.exist?(path)

      CSV.read(path, headers: true)
    rescue CSV::MalformedCSVError => e
      raise Error, "#{path} is not a readable CSV file (#{e.message}). Open it and fix the line it names."
    end

    def write(path, headers, rows)
      FileUtils.mkdir_p(File.dirname(path))
      CSV.open(path, "w") do |csv|
        csv << headers
        rows.each { |r| csv << r }
      end
    end
  end
end
