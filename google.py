import json
import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials


def load_spreadsheet():
    print 'Load Google credentials'
    json_key = json.load(open('credentials.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    gc = gspread.authorize(credentials)
    sh = gc.open_by_key('1PgxD5wx6qrWtIfnJ89fdczpS6yKK5BOZZHcRQeZCnD4')

    # delete worksheet
    sh.del_worksheet(sh.worksheet('BC105'))

    # make worksheet
    wks = sh.add_worksheet(title="BC105", rows='100', cols='10')
    #wks = sh.worksheet('105_cart')
    
    header = wks.range('A1:J1')
    #header[0].value = 'besteller'
    #header[1].value = 'artikel'
    #header[2].value = 'type'
    #header[3].value = 'sku'
    header[4].value = 'Price alert'
    header[5].value = 'Originele prijs'
    header[6].value = 'Prijs per stuk'
    header[7].value = 'Aantal'
    header[8].value = 'Totaal'
    header[9].value = '5%'
    wks.update_cells(header)

    return wks

def add_to_spreadsheet(wks, orders):
    row_number = 2

    for user, products in orders.iteritems():
        wks.update_cell(row_number, 2, user)
        row_number += 1
        first_row = row_number
        for product in products:
            row = wks.range('A' + str(row_number) + ':J' + str(row_number))
            row[0].value, row[1].value = product['name'].split(' ', 1)
            row[2].value = product['type']
            row[3].value = "=(\"" + product['sku'] + "\")"
            row[4].value = product['pa']
            row[5].value = product['original_price']
            row[6].value = product['price']
            row[7].value = product['qty']
            row[8].value = float(product['price']) * product['qty']
            row[9].value = math.ceil(float(row[5].value) * 0.95 * 100) / 100

            wks.update_cells(row)
            row_number += 1
        last_row = row_number - 1
        wks.update_cell(row_number, 9, '=SUM(I' + str(first_row) + ':I' + str(last_row) + ')')
        wks.update_cell(row_number, 10, '=CEILING(I' + str(row_number) + '*0.95, 0.01)')
        row_number += 2
        print user + ' in spreadsheet'




    print 'Orders added to spreadsheet'

def write_summary():
    print 'write summary'

