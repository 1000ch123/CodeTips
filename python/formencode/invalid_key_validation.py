# -*- coding: utf-8 -*-
import formencode


class MySchema(formencode.schema.Schema):
    name = formencode.validators.String()
    age = formencode.validators.Int()
    weight = formencode.validators.Empty()  # None,''は弾けない
    # weight = None  # validatorの無効化.allow_extra_fieldsすると通ってしまう


# あるキーを含むときinvalid
if __name__ == '__main__':
    schema = MySchema()
    #schema.ignore_key_missing = True
    #schema.allow_extra_fields = True

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
            print('------')
            print(schema.to_python(d))
        except formencode.Invalid as e:
            print(e.msg)
            #print(e.value)
