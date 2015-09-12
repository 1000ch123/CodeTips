# -*- coding: utf-8 -*-
import formencode


class MySchema(formencode.schema.Schema):
    name = formencode.validators.String()
    age = formencode.validators.Int()


# Schemaを使ったvalidation
if __name__ == '__main__':
    schema = MySchema()
    data = {
        'name': 'maki',
        'age': 17
        }
    try:
        print(schema.to_python(data))
        # print(MySchema.to_python(data))
    except:
        print('fail')