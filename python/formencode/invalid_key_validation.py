# -*- coding: utf-8 -*-
import formencode


class MySchema(formencode.schema.Schema):
    name = formencode.validators.String()
    age = formencode.validators.Int()
    # weight = formencode.validators.Empty()  # Noneは弾けない
    weight = None


# あるキーを含むときinvalid
if __name__ == '__main__':
    schema = MySchema()

    lack_data = {
        'name': 'maki',
        'age': 17,
        }
    invalid_data = {
        'name': 'maki',
        'age': 17,
        'weight': 40
        }
    null_data = {
        'name': 'maki',
        'age': 17,
        'weight': None
        }

    data = [lack_data, invalid_data, null_data]

    for d in data:
        try:
            print(schema.to_python(d))
        except formencode.Invalid as e:
            print(e.msg)
            print(e.value)
