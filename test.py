import time
import datetime
import math

# start_date = datetime.datetime(year=2022, month=11, day=8, hour=19, minute=40)
# print(start_date)
#
# start_date_in_second = time.mktime(start_date.timetuple())
# current_time_in_second = time.mktime(datetime.datetime.now().timetuple())
#
# print(start_date_in_second)
# print(current_time_in_second)
# print((start_date_in_second - current_time_in_second) / 60)
# time.mktime(d.timetuple()) из даты в секунды
# datetime.date.fromtimestamp(s) из секунд в дату

def grouping():
    tournament_teams = range(1, 17, 1)

    limit_group = 8

    groups = ['A', 'B', 'C', 'D']

    for index in range(0, len(tournament_teams), 1):
        group = groups[math.ceil((index + 1) / limit_group) - 1]
        print(f'{tournament_teams[index]} | {group}')


def add_opening_matches():
    limit_group = 8

    tournament_teams = range(1, 17, 1)

    count_groups = len(tournament_teams) // limit_group
    groups = ['A', 'B', 'C', 'D']

    for group in range(count_groups):
        tournament_teams_for_group = groups[group]
        print(tournament_teams_for_group)
        for index in range(0, limit_group, 2):
            first_team_id = tournament_teams[index]
            second_team_id = tournament_teams[index + 1]
            print(f' {first_team_id}')
            print(f' {second_team_id}')


if __name__ == '__main__':
    opening_date = datetime.datetime(day=30, month=11, year=2022,
                                     hour=12,
                                     minute=0)
    current_date = datetime.datetime.now()

    date_left = opening_date - current_date

    print(date_left)

    print(date_left.total_seconds())
