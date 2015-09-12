# -*- coding: utf-8 -*-
import formencode


# 最もシンプルなバリデーション
if __name__ == '__main__':
    data = [1, 2, '10', 'a', []]
    for d in data:
        try:
            v = formencode.validators.int()
            print(v.to_python(d))
        except formencode.Invalid as e:
            # http://www.formencode.org/en/latest/modules/api.html?highlight=invalid#formencode.api.Invalid
            print(e)
