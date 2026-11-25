# frozen_string_literal: true

module Seedbox
  # Writes one reminder letter per member who has a packet due soon.
  class Reminders
    def initialize(store: Store.new)
      @store = store
    end

    def write_all
      members = @store.members.to_h { |m| [m.id, m] }
      due_soon = @store.loans.select { |l| l.open? && Policy.remind?(l.due_on, Clock.today) }

      FileUtils.mkdir_p(Config.out_dir)
      due_soon.group_by(&:member_id).map do |member_id, loans|
        member = members[member_id]
        raise Error, "Loan #{loans.first.id} belongs to member #{member_id}, who is not in members.csv." if member.nil?

        path = File.join(Config.out_dir, "reminder-#{member_id}.txt")
        File.write(path, letter(member, loans))
        path
      end
    end

    private

    def letter(member, loans)
      lines = loans.map { |l| "  - packet #{l.packet_id}, due #{l.due_on}" }
      <<~TEXT
        Hello #{member.name},

        these seed packets are due back at the library soon:

        #{lines.join("\n")}

        Bring back seeds from your own plants if you can. If the harvest
        failed, tell us and we will close the loan.

        Written on #{Time.now.strftime("%Y-%m-%d")}.
      TEXT
    end
  end
end
