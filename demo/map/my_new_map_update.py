from my_map_mapped import Customer, Session


session = Session()

c = Customer(name="John Doe3", birthday="2000-05-31")

session.add(c)

session.commit()

