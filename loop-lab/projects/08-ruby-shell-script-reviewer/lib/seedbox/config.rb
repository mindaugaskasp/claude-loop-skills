# frozen_string_literal: true

module Seedbox
  # Where the data lives. SEEDBOX_DATA and SEEDBOX_OUT override the defaults.
  module Config
    ROOT = File.expand_path("../..", __dir__)

    def self.data_dir
      ENV.fetch("SEEDBOX_DATA", File.join(ROOT, "data"))
    end

    def self.out_dir
      ENV.fetch("SEEDBOX_OUT", File.join(ROOT, "out"))
    end

    def self.loans_file
      File.join(data_dir, "loans.csv")
    end

    def self.members_file
      File.join(data_dir, "members.csv")
    end
  end
end
