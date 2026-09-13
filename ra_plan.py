def parse_group_info(group_name):
    if not isinstance(group_name, str):
        raise ValueError("Название группы должно быть строкой")

    try:
        level_char = group_name[2]
        year = int(group_name.split("-")[-1])
    except (IndexError, ValueError):
        raise ValueError(
            f"Некорректное название группы: {group_name}"
        )

    if level_char == "Б":
        level = 1
    elif level_char == "М":
        level = 2
    else:
        raise ValueError(
            f"Неизвестный уровень обучения в группе: {group_name}"
        )

    return {
        "level": level,
        "year": year,
    }
    
def fill_new_plan(connection, group_name):
    group_info = parse_group_info(group_name)

    with connection.cursor() as cursor:
        query = """
            INSERT INTO ra_plan (
                level,
                year
            )
            VALUES (%s, %s)
            RETURNING id
        """

        cursor.execute(
            query,
            (
                group_info["level"],
                group_info["year"],
            ),
        )

        return cursor.fetchone()[0]

def get_plan_for_group(connection, group_name):
    group_info = parse_group_info(group_name)

    with connection.cursor() as cursor:
        query = """
            SELECT id
            FROM ra_plan
            WHERE level = %s
              AND year = %s
        """

        cursor.execute(
            query,
            (
                group_info["level"],
                group_info["year"],
            ),
        )

        result = cursor.fetchone()

        if result is None:
            return None

        return result[0]