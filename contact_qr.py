def build_vcard(name, phone="", email="", org=""):
    if name.strip() == "":
        raise ValueError("Naam khali hai")

    lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{name}"]

    if phone:
        lines.append(f"TEL:{phone}")
    if email:
        lines.append(f"EMAIL:{email}")
    if org:
        lines.append(f"ORG:{org}")

    lines.append("END:VCARD")
    return "\n".join(lines)


if __name__ == "__main__":
    print(build_vcard("Shashi", "9876543210", "a@b.com", "RCET"))