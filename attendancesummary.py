# enter a name
# set start time
# set grace period
# set end time
# set time entered
# output > 
# name | 2023/04/24 
# -----| ---------
# nicoh | attended
# barrios | late
import pandas as pd
from datetime import date as dt, datetime, time, timedelta

# create today's dataframe
def attendance_initial():
    # add column names, {todays date}
    df = pd.DataFrame(columns=['name', dt.today().strftime("%Y-%m-%d")])

    # save to csv
    df.to_csv('CSC 0321-1.csv', index=False)

# add entrys for today
def attendance_column(name, time_st, gp, time_end, TIME_IN):

    cur_date = dt.today().strftime("%Y-%m-%d")
    attd_list = []
    
    # import csv change
    attendance_csv = pd.read_csv('CSC 0321-1.csv')

    # cur_time = dt.today().strftime('%H:%M:%S')
    cur_time = datetime.strptime(TIME_IN, '%H:%M:%S')
    cur_time_only = cur_time.strftime('%H:%M:%S')
    
    # convert string to datetime
    time_end_st = datetime.strptime(time_end, '%H:%M:%S')
    time_end_only = time_end_st.strftime('%H:%M:%S')
    
    time_st_cv = datetime.strptime(time_st, '%H:%M:%S')
    total_time_start = time_st_cv + timedelta(minutes=gp)
    total_time_only = total_time_start.strftime('%H:%M:%S')

    # if current entry is less than grace period mark attended
    if cur_time_only <= total_time_only and cur_time_only <= time_end_only:
        # add to list
        attd_list = [name, 'Attended']

        # add list to dataframe
        attendance_csv.loc[len(attendance_csv)] = attd_list
    elif cur_time_only > total_time_only and cur_time_only <= time_end_only:
        attd_list = [name, 'Late']
        attendance_csv.loc[len(attendance_csv)] = attd_list

    # drop duplicates
    attendance_csv = attendance_csv.drop_duplicates(subset='name')

    # write to csv
    attendance_csv.to_csv('CSC 0321-1.csv', index=False)

# connect all dataframe into one big summary
def attendance_summary():
    attd_summary = pd.read_csv('attd_summary.csv')

    attendance = pd.read_csv('CSC 0321-1.csv')

    attd_summary = pd.merge(attd_summary, attendance, 
                            on='name', how='inner', 
                            suffixes=('','_remove'))

    attd_summary.drop([i for i in attd_summary.columns if 'remove' in i], 
                                     axis=1, inplace=True)
    
    print(f'AttendanceS: \n{attd_summary}')

    attd_summary.to_csv('attd_summary.csv', index=False)


# attendance_initial()

attendance_column('Barrios', '10:00:00', 30, '12:00:00', '10:10:00')
attendance_column('Antonio', '10:00:00', 30, '12:00:00', '10:20:00')
attendance_column('Ngo', '10:00:00', 30, '12:00:00', '11:10:00')
attendance_column('Borlat', '10:00:00', 30, '12:00:00', '10:30:00')
attendance_column('Gundayao', '10:00:00', 30, '12:00:00', '10:00:00')

attendance_summary()