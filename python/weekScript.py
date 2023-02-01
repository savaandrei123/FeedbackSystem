from datetime import datetime, timedelta

date_list = []


def print_list(list):
    for week_nr, date in enumerate(list):
        print(datetime.strftime(date[0], "%d/%m/%Y") + " -- " + datetime.strftime(
            date[1], "%d/%m/%Y") + " -- Saptamana ", week_nr+1)


def calculate_weeks(start, weeks):
    year_start = datetime.strptime(start, "%d/%m/%Y").date()
    begining = year_start
    begining = generate_intervals(weeks[0], begining)
    begining = begining + timedelta(days=weeks[1]*7)
    begining = generate_intervals(weeks[2], begining)
    begining = begining+timedelta(days=weeks[3]*7)
    begining = begining+timedelta(days=weeks[4]*7)
    begining = generate_intervals(weeks[5], begining)
    begining = begining+timedelta(days=weeks[6]*7)
    begining = generate_intervals(weeks[7], begining)
    return date_list


def generate_intervals(week_nr, begining):
    for x in range(week_nr):
        end = begining + timedelta(days=6)
        date_list.append([begining, end])
        begining = end + timedelta(days=1)
    return begining
