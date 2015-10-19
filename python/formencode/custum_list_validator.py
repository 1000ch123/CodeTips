# -*- coding: utf-8 -*-
import formencode


class MyListValidator(formencode.FancyValidator):
    def _convert_to_python(self, value, state):
        try:
            if isinstance(value, list):
                return value
            # elseでInvalidをraiseすると下のexceptに捕まる..
        except:
            print('error')
            raise formencode.Invalid('wrong type', value, state)
        raise formencode.Invalid('missing maki', value, state)


# 最もシンプルなバリデーション
if __name__ == '__main__':
    data = ['maki', 'nico', 'nikomaki', 'temakizushi', 1, None]
    v = MyListValidator()

    try:
        print(v.to_python(data))
    except formencode.Invalid as e:
        print(e)
