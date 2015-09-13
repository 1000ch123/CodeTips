# formencode 思想

- validation & conversion
    - ２つが同時に起こる
    - conversionできない = error発生 = vinvalid
- conversion
    - to_python
        - stringなどの入力をPythonデータ型として変換
    - from_python
        - Pythonデータ型を何かに変換
- form generation もあるって
    - htmlfill
    - データのデフォルト値設定するものぽいけど
    - formが何で作られていようが共通して利用できるということかな
    -
