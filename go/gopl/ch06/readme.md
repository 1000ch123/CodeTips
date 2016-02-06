# chapter6 method

- OOP流行ってる
- object
    - value
    - method = function
- Goにおけるカプセル化とコンポジションをみていこう

# 6.1 method declarations

- goの「メソッド」定義の話

- function定義にパラメタ１つ追加
    - レシーバとなるオブジェクトの型を指定
- thisとかselfは使わないよ
    - Java...Python...
- method定義の中ではレシーバ型のはじめの１文字を使うことが多いらしい
    - Point なら p
- レシーバのプロパティには`.`でアクセス可能
    - いわゆるセレクタ
    - structと一緒ね
- プロパティとメソッドは同じ名前空間なので，同名定義はダメ

- functionが引数と返り値の組で型を持つように，methodはrecieverの型が加わると思えばよかろう


```
type Point struct{ X, Y float64 }

func (p Point) Distance(q Point) float64 {
    return ...
}
```

- メソッドは型ごとに名前空間があるので，別型なら同名メソッド定義ok
    - class定義の中に書くのではなく，レシーバ指定してmethod定義
    - C++ぽさはある
- 任意の named type がrecieverになれる
    - ただし，ベースがpointer, interfaceの場合はダメらしい
    - interfaceについてはch7で

- メソッドは必ずobjectへのメッセージとして利用される
    - よって過度に説明的にする必要はない
        - x : p.PointDistance
        - o : p.Distance
    - functionの場合，calcPointDistanceみたいになるので面倒だね
- 外から利用する場合，package名指定するのはobj生成時のみ
    - 実際にmethod利用するときはpackage名指定いらないので便利
    - functionだとpackage指定で呼ぶ必要あり

# 6.2 methods with a pointer reciever

- 自身に副作用を与えるmethod定義の話

- function call 時，基本は値渡し
    - copyされる
    - objの状態更新するmethodかけない..
- recirever には named type への pointer を指定できる

- 関数名としては `(*Point).ScaleBy` みたいな感じ
    - `*Point.ScalyBy` は `*(Point.ScaleBy)` と解釈

```
func (p *Point) ScaleBy(factor float64) {
    p.X *= factor
    p.Y *= factor
}
```

- named type の pointer は reciever になれる
- pointer を named type にしたものは reciever になれない

- pointer への method 呼び方いろいろある(p158)
- けど，便利なようにaliasがある(p158下)
    - 型に対するmethodはpointerに対して呼べるし，逆も然り
    - p159 中段にまとめあるので確認

- pointerへのmethodでなければ，コピーしたinstanceに対して呼んでok
- poitnerへのmethodは，オリジナルのデータ書き換える可能性あるので気をつけろ

## 6.2.1 nil is a valid reciever type

- nilが価値あるzero値である型Tの場合
    - Tに対するmethodはnilについて呼んでもok
    - linked listとか
- ex p160下
    - Getはok,Addはダメ？なんで？
    - addの内部処理のappendのとこぽい
    - v = {} ならよいけど nilはダメみたいな感じなのだろうか...

# 6.3 composing types by struct embedding

- struct 埋め込みした時のmethod挙動の話

- 4.4.3 で見たのといっしょ
- property同様，methodもembedした型に対して呼べる
    - 先に自身のものを探し，なければembedしたものを探す
    - 同階層に同名があるとダメ p163頭
- ただし，あくまでhas-aであり，is-aではない p162頭
    - ので，引数として渡すことはできない
    - 渡したければ，embedした型を明示的に渡す必要がある
- embeddingにより，無名structに対してもmethod呼べる p164
    - 独自struct作っていいんじゃないかなーと思うけど..メモリ的な問題かな


# 6.4 method values and expressions

- メソッドを値として扱う時の話

- <selector>.<method> で method value
    - curry化された関数，みたいな扱いができる（ちょっと違うけど
    - 値なので変数代入可能
    - 引数として高階関数に渡したりもできる
        - それくらいしか使いみち思いつかないな..

- <type>.<method> でmethod expression
    - fn(<reciever>, args) な 関数が取得できる
    - クラスメソッド的な使い方ができるんかな
    - 様々なrecieverにmethod呼びたい時とかに使えるらしいが
        - こんなのもできるよー程度でいいんじゃないかなー..

# 6.5 example bit vector type

- エクササイズの話

- set型のシミュレート
    - 通常はmap使えばいい
    - 要素が正の整数で集合演算が多い場合など，bid vectorという構造が使える
    - setにiが含まれるとき，wordsの i番目のbitが1になる
        - イメージ: 1001 = {1,4}
- れっつexercize!
    - 問題数少ないけど実装結構あるぞw

# 6.6 encapsulation

- goにおけるpackageの名前空間の話と，一般的なカプセル化の話

- 基本的に名前の１文字目の大文字小文字でアクセス範囲変わる
    - upper : public
    - lower : private

- objectを定義するときはstructを使うと良い
    - プロパティがカプセル化される
    - ただし同packageではアクセス可能
    - 値についてあれこれするときはmethod経由にする感じ

- p169以降は一般的なカプセル化の話なので各自どうぞ
    - getter書くときはgetとかかかなくていいよ
