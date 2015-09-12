# -*- coding: utf-8 -*-
import formencode


# 最もシンプルなバリデーション
if __name__ == '__main__':
    data = [1, 2, '10', 'a', []]
    for d in data:
        try:
            v = formencode.validators.Int()
            print(v.to_python(d))
        except:
            print('fail')
