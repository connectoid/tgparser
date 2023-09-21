link = 'https://t.me/proparsing'
if link.startswith('https://t.me/'):
    link = link.replace('https://t.me/', '@')
print(link)