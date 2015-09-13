# -*- coding: utf-8 -*-
import formencode


# 最もシンプルなバリデーション
if __name__ == '__main__':
    data = ['foo', 'hi', 'hoge']
    v = formencode.All(
        formencode.validators.String(),
        formencode.validators.MaxLength(3)
        )

    # この程度ならこんなかんじでもok
    # v = formencode.validators.String(max=3)

    for d in data:
        try:
            print(v.to_python(d))
        except formencode.Invalid as e:
            print(e)
