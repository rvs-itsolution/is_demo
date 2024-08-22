def get_status(code: str) -> str:
    """
    Функция для возврата текстового описания задачи по его коду.
    """
    match code:
        case '1':
            res = 'Новая'
        case '2':
            res = 'В ожидании'
        case '3':
            res = 'Выполняется'
        case _:
            res = 'Предположительно выполнена'
    return res
