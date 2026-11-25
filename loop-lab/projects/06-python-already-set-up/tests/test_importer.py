import pytest

from nudge.importer import ImportProblem, read_appointments

HEADER = "patient_name,phone,starts_at,clinician\n"


def write(tmp_path, body):
    path = tmp_path / "appointments.csv"
    path.write_text(HEADER + body, encoding="utf-8")
    return path


def test_reads_a_good_row(tmp_path):
    path = write(tmp_path, "Rasa,+37060000001,2026-11-02 09:30,Dr. Jonaitis\n")
    (appointment,) = read_appointments(path)
    assert appointment.phone == "+37060000001"
    assert (appointment.starts_at.hour, appointment.starts_at.minute) == (9, 30)


def test_skips_a_row_with_a_local_phone_number(tmp_path):
    path = write(tmp_path, "Rasa,860000001,2026-11-02 09:30,Dr. Jonaitis\n")
    assert read_appointments(path) == []


def test_a_bad_start_time_says_which_row(tmp_path):
    path = write(tmp_path, "Rasa,+37060000001,next Monday,Dr. Jonaitis\n")
    with pytest.raises(ImportProblem, match="Row 2"):
        read_appointments(path)
