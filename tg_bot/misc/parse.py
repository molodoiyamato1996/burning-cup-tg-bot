async def parse_callback(method: str, callback_data: str) -> dict:
    data = callback_data.replace(f'{method}?', '')

    result = dict()

    if '&' in data:
        for item in data.split('&'):
            prop = item.split('=')
            result[prop[0]] = prop[1]
    else:
        prop = data.split('=')
        result[prop[0]] = prop[1]

    return result