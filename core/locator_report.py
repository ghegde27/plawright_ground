class LocatorReport:
    _outdated = []

    @classmethod
    def mark_outdated(cls, page, element, old_locator, new_locator):
        cls._outdated.append({
            "page": page,
            "element": element,
            "old": old_locator,
            "new": new_locator
        })

    @classmethod
    def generate_report(cls):
        if not cls._outdated:
            return "No locator changes detected."

        lines = ["\n===== LOCATOR UPDATE REPORT ====="]
        for item in cls._outdated:
            lines.append(
                f"[{item['page']}] {item['element']}\n"
                f"   OLD → {item['old']}\n"
                f"   NEW → {item['new']}\n"
            )
        return "\n".join(lines)
