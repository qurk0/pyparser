import normalization as n


def fill_ra_control(
    connection,
    plan_id,
    semester,
    controls,
    disc_ids,
):
    with connection.cursor() as cursor:
        for control in controls:
            disc_id = disc_ids.get(
                control.discipline.title
            )

            if disc_id is None:
                raise ValueError(
                    f"Не найдена дисциплина "
                    f"'{control.discipline.title}'"
                )

            max_grade = n.TYPE_GRADE_MAPPING.get(
                control.control_type
            )

            if max_grade is None:
                raise ValueError(
                    f"Неизвестный тип контроля "
                    f"'{control.control_type}'"
                )

            # дальше твой INSERT без изменений
            insert_query = """
                INSERT INTO ra_control (
                    plan_id,
                    disc_id,
                    sem,
                    form,
                    max_grade
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """
            cursor.execute(
                insert_query,
                (
                    plan_id,
                    disc_id,
                    semester,
                    control.control_type,
                    max_grade,
                ),
            )
            inserted_id = cursor.fetchone()[0]
            print(
                f"[+] Данные успешно добавлены "
                f"в ra_control с id: {inserted_id}!"
            )

def get_control_id_by_disc_plan_form_sem(
    connection,
    plan_id,
    disc_id,
    form,
    sem,
):
    with connection.cursor() as cursor:
        query = """
            SELECT id
            FROM ra_control
            WHERE disc_id = %s
              AND form = %s
              AND plan_id = %s
              AND sem = %s
        """

        cursor.execute(
            query,
            (
                disc_id,
                form,
                plan_id,
                sem,
            ),
        )

        result = cursor.fetchone()

        if result is None:
            return None

        return result[0]