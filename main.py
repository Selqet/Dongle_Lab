from tkinter import ttk
from tkinter import *
import wmi
from custom_exceptions import *

def check_if_plugged_and_get_device_id(c):
    for disk in c.query('SELECT * FROM Win32_DiskDrive WHERE Model LIKE "TDKMedia Trans-It Drive USB Device"'):
        deviceID = disk.DeviceID
        return deviceID
    raise KeyNotFoundException

def check_serial_number(c):
    for disk in c.query('SELECT * FROM Win32_DiskDrive WHERE Model LIKE "TDKMedia Trans-It Drive USB Device"'):
        serialNumber = disk.SerialNumber
        if (serialNumber == '07B218030AA612FA'):
            print("Key's serial number is correct.")
        else:
            raise CorruptedSerialNumberException
    
def get_drive_letter():
    c = wmi.WMI ()
    deviceID = check_if_plugged_and_get_device_id(c)
    print('Key found. Processing...')

    check_serial_number(c)

    for partition in c.query('ASSOCIATORS OF {Win32_DiskDrive.DeviceID="' + deviceID + '"} WHERE AssocClass = Win32_DiskDriveToDiskPartition'):
        for logical_disk in c.query('ASSOCIATORS OF {Win32_DiskPartition.DeviceID="' + partition.DeviceID + '"} WHERE AssocClass = Win32_LogicalDiskToPartition'):
            return logical_disk.DeviceID


def check_key(let):
    f = open(f'{let}\\key.selqet', 'r')

    if (f.read() == 'loremipsumdolorsitamet'):
        print("Code is correct. Welcome, admin.")
    else:
        raise IncorrectCodeException
    f.close()   

#idVendor=0x0718, idProduct=0x0629
def authorization():
    try:
        drive_letter = get_drive_letter()
    except KeyNotFoundException:
        print('Key not found!')
        return
    except CorruptedSerialNumberException:
        print('Key is corrupted!')
        return

    try:
        check_key(drive_letter)
    except FileNotFoundError:
        print('Code not found!')
        return
    except IncorrectCodeException:
        print('Incorrect code!')
        return



root = Tk()
root.config(height=200, width=200)
ttk.Button(root, text="Verify", command=authorization).place(x=100, y=100,anchor=CENTER)
root.mainloop()



