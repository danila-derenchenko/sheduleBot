import asyncio

from aiohttp import ClientSession
from ujson import loads


session: ClientSession = None
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Referer": "https://samgtu.ru/students/schedule",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5"
}


async def get_groups(faculty: str | int, course: str | int):
    global session, headers
    if session is None:
        session = ClientSession()
    result = []
    try:
        result = loads(await (await session.get(f"https://samgtu.ru/students/getgrouplist?Course={course}&Faculty={faculty}", headers=headers)).text())
    except:
        pass
    return result


async def get_schedule(group_id: int | str) -> None:
    global session, headers
    if session is None:
        session = ClientSession()
    result = []
    week = (await(await session.get("https://samgtu.ru/students/schedule", headers=headers)).text()).split(" неделя (текущая)")[0].split(" ")[-1].split(">")[1]
    try:
        result = loads(await (await session.get(f"https://samgtu.ru/students/getschedule?GroupID={group_id}&WeekNumber={week}", headers=headers)).text())["wd"]
    except:
        pass
    # 1,2,3,4,5,6,7 - дни недели (ключи)
    for i in range(1, 8):
        print("\n", result[f"{i}"]["Name"])
        # существует 8 пар 1 - 8
        for j in range(1, 9):
            # Если список содержит что-то внутри:
            if result[f"{i}"]["at"][f"{j}"].get("Cells", []):
                # Вывод названия + времени
                # Возможно парсить через BS4, html - режим
                print("-> ", result[f"{i}"]["at"][f"{j}"].get("Cells", [])[0]["CellName"], "===TIME===", result[f"{i}"]["at"][f"{j}"].get("Cells", [])[0]["AuditoriumTimeName"])


loop = asyncio.get_event_loop()
loop.run_until_complete(get_schedule("29567"))
input("Продолжить показ: ")
loop.run_until_complete(get_schedule("30425"))
loop.close()