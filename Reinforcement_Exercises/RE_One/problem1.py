# problem1.py

def only_truthy(**kwargs) -> dict:

    new_dict = dict()
    for key, value  in kwargs.items():
        if value:
            new_dict["_"+key] = value

    return new_dict
