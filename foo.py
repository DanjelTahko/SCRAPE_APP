

companys = "3,768"

c = int(companys.replace(',', ''))
get_pages = lambda c : int(c/25) + 1 if (c % 25 > 0) else int(c/25)
page = get_pages(c)
print(page)