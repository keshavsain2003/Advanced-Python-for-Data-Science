def clean_data(a):
    def inner_function(*args):
        print("cleaning data")
        print("call insett_db function")
        a(*args)

    return inner_function


# @accept_values
@clean_data  # result = clean_data(insert_db), result()
def insert_db(value, value1):
    print(f"executing {value}")


# result = clean_data(insert_db)
# result("this line")

insert_db("this line", "and also this line")
