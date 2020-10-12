from csv import writer

def putToCsv(csv_file, entry):
    with open(csv_file, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(entry)

def creteCsvFile(csv_file, header):
    with open(csv_file, 'w', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(header)