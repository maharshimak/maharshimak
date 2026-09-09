import re


FORBIDDEN = {
    "insert", "update", "delete", "drop", "alter", "create", "replace",
    "truncate", "attach", "detach", "pragma", "vacuum", "reindex",
    "grant", "revoke", "commit", "rollback", "savepoint",
}


class UnsafeQueryError(ValueError):
    pass


def normalize_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.strip().rstrip(";")).strip()


def _tokens(sql: str) -> set[str]:
    return set(re.findall(r"[A-Za-z_]+", sql.lower()))


def validate_read_only(sql: str, max_rows: int = 200) -> str:
    normalized = normalize_sql(sql)
    lowered = normalized.lower()

    if not normalized:
        raise UnsafeQueryError("SQL cannot be empty.")

    if ";" in normalized:
        raise UnsafeQueryError("Multiple statements are not allowed.")

    first = lowered.split(maxsplit=1)[0]
    if first not in {"select", "with"}:
        raise UnsafeQueryError("Only SELECT or WITH queries are allowed.")

    blocked = sorted(_tokens(normalized).intersection(FORBIDDEN))
    if blocked:
        raise UnsafeQueryError(f"Forbidden SQL operation(s): {', '.join(blocked)}")

    match = re.search(r"\blimit\s+(\d+)\b", lowered)
    if match:
        current = int(match.group(1))
        if current > max_rows:
            normalized = re.sub(
                r"\blimit\s+\d+\b",
                f"LIMIT {max_rows}",
                normalized,
                flags=re.I,
            )
        return normalized

    return f"{normalized} LIMIT {max_rows}"
