# -*- coding: utf-8 -*-
import formencode


class MyValidator(formencode.FancyValidator):
    def _convert_to_python(self, value, state):
        try:
            if 'maki' in value:
                return value
            # elseでInvalidをraiseすると下のexceptに捕まる..
        except:
            print('error')
            raise formencode.Invalid('wrong type', value, state)
        raise formencode.Invalid('missing maki', value, state)


# 最もシンプルなバリデーション
if __name__ == '__main__':
    data = ['maki', 'nico', 'nikomaki', 'temakizushi', 1, None]
    v = MyValidator()
    for d in data:
        print('---')
        try:
            print(v.to_python(d))
        except formencode.Invalid as e:
            print(e)
