import pandas as pd
import datetime as dt
from datetime import timedelta
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


"""constants"""
MY_EMAIL = "vishalkumar.mit@gmail.com"
PASSWORD = "PASSWORD"
SEC_PASS = "srofrolevxynjuio"
MY_PASSWORD = os.environ.get("SEC_PASSWORD")



"""intiations of date, data reading etc."""
now = dt.datetime.now()
today = now.day
current_month = now.month
current_yr = now.year
formated_current_date = now.date().strftime("%d-%m-%Y")
see_masts_data = pd.read_csv("mast_aoh_data.csv")
last_yr_maint_dates = see_masts_data["FY21-22"]
print(last_yr_maint_dates)

overdue_series_for_this_yr = see_masts_data[see_masts_data["FY22-23"] == "overdue"]
no_overdue_series_for_this_yr = len(overdue_series_for_this_yr)
print(no_overdue_series_for_this_yr)





main_on_last_yr_for_upcoming_month = []
next_month_overdue_dates = []
masts_types = []
location_no = []
for (index, row) in see_masts_data.iterrows():
    date_str = row["FY21-22"]
    try:
        date_obj = dt.datetime.strptime(str(date_str), "%d-%m-%Y")
        if current_month == int(date_obj.month) - 1:
            main_on_last_yr_for_upcoming_month.append(f"{date_obj.day}/{date_obj.month}/{date_obj.year}")
            next_month_overdue_dates.append(f"{date_obj.day + 1}/{date_obj.month}/{date_obj.year + 1}")
            masts_types.append(row["Mast type"])
            location_no.append(row["Location"])
    except Exception as e:
        pass

print(main_on_last_yr_for_upcoming_month)
print(masts_types)
print(location_no)
"""logic for last date of current month"""
first_of_month = dt.datetime(day=1, month=current_month+1, year=current_yr)
del_time = timedelta(days=-1)
last_day_of_current_month = first_of_month + del_time
print(last_day_of_current_month)


# creating dictioary
sonpur_masts = {
    "Mast type.": masts_types,
    "location no.": location_no,
    "last maintenance": main_on_last_yr_for_upcoming_month,
    "Overdue date": next_month_overdue_dates,
}

"""creating dataframe"""
desired_output = isolator_overdue_sonpur = pd.DataFrame(sonpur_masts)
# print(f"last day of this month is {last_day_of_current_month.date()}")
masts_csv_file = isolator_overdue_sonpur.to_csv("sonpur_masts.csv")
# print(desired_output)


# def email_quotes(input):
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(user=MY_EMAIL, password=MY_PASSWORD)
#
#         connection.sendmail(
#             from_addr=MY_EMAIL,
#             to_addrs="SSEREGR215@GMAIL.COM",
#             msg=f"subject:Sonpur Masts AOH data for upcoming month\n\n{desired_output}"
#         )
#

def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText("pfa", 'plain')
    msg['Subject'] = "Sonpur Masts AOH data for upcoming month"
    msg['From'] = MY_EMAIL
    msg['To'] = "sseregr215@gmail.com"
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open("sonpur_masts.csv", 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name="sonpur_masts.csv"))

    # Create SMTP object
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)

            connection.sendmail(msg['From'], msg['To'], msg.as_string())

    # Convert the message to a string and send it

            # connection.quit()

send_mail()
# if now.date()==last_day_of_current_month.date():
#
#     email_quotes(desired_output)
# email_quotes(desired_output)
