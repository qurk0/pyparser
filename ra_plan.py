def parse_group_info(group_name):
    # У нас группа имеет вид КМ_О-ХХ-ХХ
    # нас интересует символ _ (уровень обучения) и вторые ХХ (год поступления)
    try:
        data = {}
        level_char = group_name[2] # Берем третий символ названия группы
        if level_char == "Б": 
            data["level"] = 1
        elif level_char == "М":
            data["level"] = 2
        else:
            raise ValueError("Неккоректное название группы")
    
        data["year"] = int(group_name.split("-")[-1])
        return data    
    
    except Exception as e:
        print(f"[!] Ошибка при разборе названия группы: {e}")
        return None
    
def fill_new_plan(connection, group_name):
    data = parse_group_info(group_name=group_name)
    try:
        cursor = connection.cursor()
        select_query = '''
        SELECT * FROM ra_plan
        WHERE level = %s AND year = %s;
        '''
        cursor.execute(select_query, (data["level"], data["year"]))
        if cursor.fetchall() == []:
            insert_query = '''
            INSERT INTO ra_plan (level, year)
            VALUES (%s, %s)
            RETURNING id;
            '''

            cursor.execute(insert_query, (data["level"], data["year"]))
            inserted_id = cursor.fetchone()[0]
            connection.commit()

            return inserted_id
        
    except Exception as e:
        print(f"[!] Ошибка при внесении данных в таблицу : {e}")
        connection.rollback()
        return None
    finally: 
        cursor.close()

def get_plan_for_group(connection, group_name):
    try:
        # Разбираем название группы, чтобы получить уровень обучения и год поступления
        group_info = parse_group_info(group_name)
        if not group_info:
            print("[!] Ошибка: не удалось разобрать название группы.")
            return None

        level = group_info["level"]
        year = group_info["year"]

        # Выполняем запрос к таблице ra_plan
        cursor = connection.cursor()
        select_query = '''
        SELECT id FROM ra_plan
        WHERE level = %s AND year = %s;
        '''
        cursor.execute(select_query, (level, year))
        result = cursor.fetchone()

        if result:
            plan_id = result[0]
            print(f"[+] Найден учебный план с id: {plan_id} для уровня {level} и года {year}.")
            return plan_id
        else:
            print(f"[!] Учебный план для уровня {level} и года {year} не найден.")
            inserted_id = fill_new_plan(connection, {"level": level, "year": year})
            return inserted_id
    except Exception as e:
        print(f"[!] Ошибка при получении учебного плана: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
