# -*- coding: utf-8 -*-
import formencode


class UnexpectedValidator(formencode.FancyValidator):
    def _convert_to_python(self, value, state):
        print('hello')
        raise formencode.Invalid('unexpected key', value, state)


class MySchema(formencode.schema.Schema):
    name = formencode.validators.String()
    age = formencode.validators.Int()
    weight = UnexpectedValidator()

# あるキーを含むときinvalid
if __name__ == '__main__':
    schema = MySchema()
    schema.ignore_key_missing = True

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
        'weight': ''
        }

    data = [lack_data, invalid_data, null_data]

    for d in data:
        try:
            print('------')
            print(schema.to_python(d))
        except formencode.Invalid as e:
            print(e.msg)
            #print(e.value)
