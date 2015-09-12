# -*- coding: utf-8 -*-
import formencode


# 配列のバリデーション
if __name__ == '__main__':
    data = [1, 2, 3, 4]
    try:
        v = formencode.foreach.ForEach(formencode.validators.Int())
        print(v.to_python(data))
    except:
        print('fail')
