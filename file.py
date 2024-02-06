"""
CREATED BY B20DCCN728 - MARK LORENZO
------------------------------------------------
"""


def get_data(file_path: str) -> list[dict[str, str, str]]:
    data = []
    with open(file_path, "r") as file:
        for line in file:
            email, password, recovery_mail = line.strip().split("|")
            data.append({
                "email": email,
                "password": password,
                "recovery_mail": recovery_mail
            })
    return data
