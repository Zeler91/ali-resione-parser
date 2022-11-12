import sqlitemanager as sqlm

data = sqlm.select_data('SELECT * FROM resione DESC LIMIT 1', False)

print(data)