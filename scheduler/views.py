import random
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from django.core.mail import send_mail
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create your views here.

class VerifyError(Exception):
    pass


def my_job():
    print(1)


def verify_dates(date1: str, date2: str, date_format='%Y-%m-%d') -> bool:
    """
    Verify if date1 is no longer than 6 days ahead of date2.
    :param date1: date string in 'date_format' format.
    :param date2: date string in 'date_format' format.
    :param date_format: date format string. Default is '%Y-%m-%d' (ISO 8601 date format).
    :return: True if date1 is no longer than 6 days ahead of date2, False otherwise.
    """
    # Parse the date strings into datetime objects
    dt1 = datetime.strptime(date1, date_format) - timedelta(weeks=1)
    dt2 = datetime.strptime(date2, date_format)

    # Calculate the difference in days between the two dates
    diff = (dt2 - dt1).days

    # Return whether the difference is less than or equal to 6
    return diff <= 6


def is_date_in_list(date_list, single_date):
    return single_date in date_list


def convert_time(time):
    """Converts a time string in 'hh:mmpm/am' format to a datetime object."""
    return datetime.strptime(time, "%I:%M%p")


def find_closest_time(time_list, target_time):
    """Finds the closest time in time_list to the target_time."""
    target_time = datetime.strptime(target_time, "%H:%M:%S")

    # Convert all times in time_list to datetime objects
    time_list = [convert_time(time) for time in time_list]

    # Find the time in time_list that is closest to target_time
    closest_time = min(time_list, key=lambda time: abs(target_time - time))

    # Convert the closest time back to the original string format
    return datetime.strftime(closest_time, "%I:%M%p").lstrip("0")


class DateNotFoundException(Exception):
    pass


def check_element_exist(str, driver):
    try:
        element = driver.find_element(By.XPATH, str)
        return True
    except:
        return False


def wait_until(target_time, offset=timedelta(0)):
    """
    Make the program wait until the local time (plus offset) reaches the specified target time.
    """
    # Combine the target_time with today's date
    target_datetime = datetime.combine(date.today(), target_time)
    while True:
        now = datetime.now() + offset
        if now >= target_datetime:
            break
        time.sleep(0.1)


def book_golf(url, username, password, date_time, date, email, date1, date2, bool1, thread, start_time, offset):
    # if not verify_dates(date1, date2):
    #     raise VerifyError('Verify is failed')
    # else:
    if bool1:
        # Specify the path to the web driver executable
        opts = ChromeOptions()
        opts.add_argument("--window-size=800,800")
        driver = webdriver.Chrome(options=opts)
        # Perform the login
        driver.get(url)
        WebDriverWait(driver, timeout=4).until(EC.visibility_of_element_located((By.ID, "login_email")))
        username_field = driver.find_element(By.ID, "login_email")
        password_field = driver.find_element(By.ID, "login_password")
        username_field.send_keys(username)
        password_field.send_keys(password)
        WebDriverWait(driver, timeout=4).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="submit_button"]/input')))
        wait_until(start_time, offset)
        print('wait_until at Local timestamp:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'   '+thread)
        driver.find_element(By.XPATH, '//*[@id="submit_button"]/input').click()
        WebDriverWait(driver, timeout=4).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="date-menu"]')))
        date_menu = driver.find_element(By.XPATH, '//*[@id="date-menu"]')
        date_menu_select = Select(date_menu)
        # date_wait_counter = 0
        # while is_date_in_list(date_menu.text, convert_date_format(str(date))) is False and date_wait_counter < 30:
        #     driver.refresh()
        #     print('date refresh, thread '+thread)
        #     WebDriverWait(driver, timeout=10).until(
        #         EC.visibility_of_element_located((By.XPATH, '//*[@id="date-menu"]')))
        #     date_menu = driver.find_element(By.XPATH, '//*[@id="date-menu"]')
        #     date_wait_counter += 1
        #     if date_wait_counter == 30:
        #         raise DateNotFoundException
        #         return False

        date_menu_select.select_by_visible_text(convert_date_format(str(date)))
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="nav"]/div/div[3]/div/div/a[4]')))
        player_menu = driver.find_element(By.XPATH, '//*[@id="nav"]/div/div[3]/div/div/a[4]')
        player_menu.click()
        WebDriverWait(driver, timeout=4).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="times"]/div'
                                                                                           '/div[ '
                                                                                           '2]/div/div/div/div['
                                                                                           '1]/div[ '
                                                                                           '1]/div[1]')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tee_time_elements = soup.find_all(class_='booking-start-time-label')
        tee_times = [tee_time.text.strip() for tee_time in tee_time_elements]
        book_time = find_closest_time(tee_times, str(date_time))
        # Submit the booking for the desired tee time
        booking_button_xpath = '//*[@id="times"]/div/div[' + str(
            tee_times.index(book_time) + 1) + ']'
        booking_button = driver.find_element(By.XPATH, booking_button_xpath)
        booking_button.click()
        print('Booking job running at Local timestamp:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'   '+thread)
        time.sleep(0.5)
        while check_element_exist('//*[@id="book_time"]/div'
                                  '/div[2]/div[5]/div[1]/div/a['
                                  '1]', driver) is not True:
            driver.refresh
            print('duplicate date selected, refresh ' + thread)
            WebDriverWait(driver, timeout=10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="date-menu"]')))
            date_menu = driver.find_element(By.XPATH, '//*[@id="date-menu"]')
            date_menu_select = Select(date_menu)
            date_menu_select.select_by_visible_text(convert_date_format(str(date)))
            WebDriverWait(driver, timeout=10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="nav"]/div/div[3]/div/div/a[4]')))
            player_menu = driver.find_element(By.XPATH, '//*[@id="nav"]/div/div[3]/div/div/a[4]')
            player_menu.click()
            WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="times"]/div'
                                                                                                '/div[ '
                                                                                                '2]/div/div/div/div['
                                                                                                '1]/div[ '
                                                                                                '1]/div[1]')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tee_time_elements = soup.find_all(class_='booking-start-time-label')
            tee_times = [tee_time.text.strip() for tee_time in tee_time_elements]
            book_time = find_closest_time(tee_times, str(date_time))
            # Submit the booking for the desired tee time
            booking_button_xpath = '//*[@id="times"]/div/div[' + str(
                tee_times.index(book_time) + 1) + ']'
            booking_button = driver.find_element(By.XPATH, booking_button_xpath)
            booking_button.click()
            time.sleep(random.uniform(0.1, 1.0))
        WebDriverWait(driver, timeout=4).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="book_time"]/div'
                                                        '/div[2]/div[5]/div[1]/div/a['
                                                        '1]')))
        print('date confirmed, tread ' + thread)
        player_button_xpath = '//*[@id="book_time"]/div/div[2]/div[5]/div[1]/div/a[4]'
        player_button = driver.find_element(By.XPATH, player_button_xpath)
        player_button.click()
        carts_button = driver.find_element(By.XPATH, '//*[@id="book_time"]/div/div[2]/div[5]/div[2]/div/a[1]')
        carts_button.click()
        book_time_button = driver.find_element(By.XPATH, '//*[@id="book_time"]/div/div[3]/button[1]')
        book_time_button.click()
        WebDriverWait(driver, timeout=4).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="payment_methods'
                                                        '"]/li[1]/label/div[1]')))
        pay_at_facility_button = driver.find_element(By.XPATH, '//*[@id="payment_methods"]/li[1]/label/div[1]')
        pay_at_facility_button.click()
        final_book_button = driver.find_element(By.XPATH, '//*[@id="payment_selection"]/div/div[3]/button[1]')
        final_book_button.click()
        WebDriverWait(driver, timeout=4).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/h1')))
        result = driver.find_element(By.XPATH, '//*[@id="content"]/div/h1')
        print('Tee time book successful, thread ' + thread)
        if result.text == 'Congratulations!':
            email_body = 'This week Golf at ' + str(date) + ' ' + str(
                book_time) + ' for player of 4' + ' is successfully booked!'
            send_mail('This weeks Golf is Successfully booked!', email_body, 'gongzhen2015@gmail.com',
                      [email])
        return True
    return False
    # return False


def ordinal(n):
    """Convert an integer into its ordinal representation."""
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def convert_date_format(date_str):
    """Convert a date string from 'YYYY-MM-DD' to 'Weekday, Mon DDth'."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime('%A, %b ') + ordinal(date.day)


def convert_time(time):
    """Converts a time string in 'h:mmpm/am' or 'hh:mmpm/am' format to a datetime object."""
    time_format = "%I:%M%p" if len(time) == 7 else "%I:%M%p"
    return datetime.strptime(time, time_format)


def find_closest_time(time_list, target_time):
    """Finds the closest time in time_list to the target_time."""
    target_time = datetime.strptime(target_time, "%H:%M:%S")

    # Convert all times in time_list to datetime objects
    time_list = [convert_time(time) for time in time_list]

    # Find the time in time_list that is closest to target_time
    closest_time = min(time_list, key=lambda time: abs(target_time - time))

    # Convert the closest time back to the original string format
    return datetime.strftime(closest_time, "%I:%M%p").lstrip("0").lower()
