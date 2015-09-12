# -*- coding: utf-8 -*-
import formencode


class MySchema(formencode.schema.Schema):
    name = formencode.validators.String()
    age = formencode.validators.Int()


# Schemaを使ったvalidation
# 独自キーを許容するか?

if __name__ == '__main__':
    schema = MySchema()

    full_data = {
        'name': 'maki',
        'age': 17
        }

    lack_data = {
        'name': 'maki',
        }

    extra_data = {
        'name': 'maki',
        'age': 17,
        'like': 'nico'
        }

    data = [
        full_data,
        lack_data,
        extra_data,
        ]

    schema.ignore_key_missing = True
    schema.allow_extra_fields = True
    schema.filter_extra_fields = False

    for d in data:
        try:
            print(schema.to_python(d))
        except formencode.Invalid:
            print('fail')
