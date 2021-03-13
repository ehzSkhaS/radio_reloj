import sys
import time
import ntplib
import datetime
from socket import gaierror, timeout

""" Windows time structure """
if sys.platform == "win32":
    from ctypes.wintypes import WORD
    from ctypes import Structure, windll, pointer


    class SYSTEMTIME(Structure):
        _fields_ = [
            ( 'wYear',            WORD ),
            ( 'wMonth',           WORD ),
            ( 'wDayOfWeek',       WORD ),
            ( 'wDay',             WORD ),
            ( 'wHour',            WORD ),
            ( 'wMinute',          WORD ),
            ( 'wSecond',          WORD ),
            ( 'wMilliseconds',    WORD ),
        ]
    SetLocalTime = windll.kernel32.SetLocalTime

""" Linux time structure """
if sys.platform.startswith('linux'):
    import ctypes
    import ctypes.util

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME 0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
                _fields_ = [("tv_sec", ctypes.c_long),
                            ("tv_nsec", ctypes.c_long)]
    librt = ctypes.CDLL(ctypes.util.find_library("rt"))


def set_windows_time(host, wait_time):
    while 1:
        try:
            connector = ntplib.NTPClient()
            response = connector.request(host, version=3)
            dt_ = datetime.datetime.fromtimestamp(response.tx_time)
            print('Got time as', dt_.strftime('%Y-%m-%d %H:%M:%S'), 'from NTP Server')
            dt_tuple = dt_.timetuple()
            st = SYSTEMTIME()
            st.wYear            = dt_tuple.tm_year
            st.wMonth           = dt_tuple.tm_mon
            st.wDayOfWeek       = (dt_tuple.tm_wday + 1) % 7
            st.wDay             = dt_tuple.tm_mday
            st.wHour            = dt_tuple.tm_hour
            st.wMinute          = dt_tuple.tm_min
            st.wSecond          = dt_tuple.tm_sec
            st.wMilliseconds    = 0
            ret = SetLocalTime(pointer(st))
            if ret == 0:
                print('Setting failed. Try as administrator.')
            else:
                print('Successfully set the systemtime')
        except (gaierror, timeout, ntplib.NTPException):
            print("Couldn't sync with ntp server...next try in: %ds" %wait_time)            
        time.sleep(wait_time)


def set_linux_time(host, wait_time):
    while 1:
        try:
            connector = ntplib.NTPClient()
            response = connector.request(host, version=3)
            ts = timespec()
            dt_ = datetime.datetime.fromtimestamp(response.tx_time)
            ts.tv_sec = int(time.mktime(datetime.datetime(*dt_.timetuple()[:6]).timetuple()))
            ts.tv_nsec = dt_.microsecond * 1000  # micro to nanosecond
            librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))
        except (gaierror, timeout, ntplib.NTPException):
            print("Couldn't sync with ntp server...next try in: %ds" %wait_time)            
        time.sleep(wait_time)


if __name__ == "__main__":
    if sys.platform == "win32":
        set_windows_time("pool.ntp.org", 5)
    if sys.platform.startswith('linux'):
        set_linux_time("pool.ntp.org", 5)
