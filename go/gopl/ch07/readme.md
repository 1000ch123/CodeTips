# chapter 7

# 7.11 descriminating errors with type assertions

- type assertion つかって Errorをみわける

- file operationかんがえよう
    - I/Oはいろんな原因でエラーしうる
    - エラーごとに対処が異なる
        - file slready exists
        - file not found
        - permission denied

- 切り分けるため，osパッケージに error 型を受け取りboo.返すヘルパー関数が3つある
    - IsExist
    - IsNotExist
    - IsPermission
    - godoc os IsExist
        - func IsExist(err error) bool
        - 引数はerror interfaceだからこの名前でいいのか...?
    - 中でどうやってきりわけるんだろうねが主題

- naiveなimpl
    - msgにある文字列が含まれているか
        - たしかにシンプルだ
    - platformごとにIOロジックは異なるのでNot Robustらしい
        - 同じ文字列がが別のエラーに含まれる可能性もあるよね
    - 開発段階ではいいけど，prodコードには入れられないかな

- structured error value としてdedicated type（それ専用の型）を用いる
    - パスに関するエラーハンドリング用: PathError
        - Op, Path, Err からなるstruct
            - godoc os PathError
    - PathError は Error メッセージに対応できるので Errorインタフェースをみたす
    - よって clientはPathErrorであることを意識せず，ふつーにErrorメソッドを呼べる

- pe, ok = err.(*PathError) 
    - で判定できる
    - キャストできれば okがTrueになるね
    - ほんで pe.errを返せば 元のerrが取り出せる

- ただ実際のコードを見ると err.(type) となっている
    - type assersion として type（型|interafce)を渡している？
    - まぁ受け取った値の型を返すとかそんな感じな気はするのだけど
    - 「type」というinterfaceがあるのかな...うーむ
        - これ，後でもでてきたわ..

# 7.12 Querying Behaviors with interface type assertions

- net/http の webサーバ,httpヘッダかくやーつっぽいコード
    - 毎度思うけど io.Writer が 「書く人」じゃなくて「書かれることができる人（writableな人）」を表すっての違和感なのだよなぁ
    - writeメッセージの受け取り手，ってことなんだろうけどさ

- io.Writer の 定義的に バイト列が必要
type Writer interface {
    Write(p []byte) (n int, err error)
} 

- しかし書き込みたいもの（header）はstring
    - よってbyteのsliceにconvertする必要がある
    - ただし，converはmemory allocationがひつよう
    - 余計なメモリ使わないで済む方法ない？が主題

- io.Writer がその定義で示すのはただ一つ
    - 「byte列をかきこめるよ」
        - 引数で示しているからね
    - WriteString メソッドもっててもいいんじゃないの！！！１
    - そのほうがmemoryてきにうれしいよね？というはなし

- 任意の io.Writer が WriteString持つことは想定できない
    - じゃーあたらしいinterfaceつくろう!

- 以下codeについて
    - func writeStringを定義する
        - 中で stringWriter interface を定義している
        - こいつは「WriteStringメソッドを持つ」ことを保証する

- 単純に「この関数持ってますのん？」をcheckするために追加 interfaceを定義しているだけの予感
    - もし writer自身がwritestring を持っているのであれば，コピーしなくてもいいよねーと
    - writer自身が実装しているwritestringの詳細次第では変わらない気もするね

- まぁ現実には 標準ライブラリにあるやつを使おう
    - godoc io WriteString
        - 内部的には stringWriter いんたふぇーすつかってるぽい


- curiousな点(p209下から.このへんよくわからん..)
    - stringWriterは WriteStringメソッドをもつことしか制限しない
    - WriteStringメソッドの動作を規定するものはない
- ふつーに考えれば
interface {
io.Writer
WriteString (s string) (n int, err error)
}
- となるべきじゃろ.というのを暗黙の了解似しているという話？
- 厳密に型を考えるとどうなの，と思うかもしれないが，実用上は問題ない
    - 偶然にinterface満たされるなんてことはそんなない

- この呼び方なら StwingWriterが Writerであることは補償されるけど，interface自体は StringWriterがWriterであるかどうかは保証できないんじゃないかな
    - まぁだからwriteStringのなかで定義されてるのかな


# 7.13 type switches

- interfaceは2通りの使い方があるよ
    - 1
       - 共通メソッド定義として，具体型の共通の性質を定義する
       - ただし実装詳細はhideする
       - まさに界面だけ，だね
       - 「methodについて」が重要なところ
       - 具体型がどうであろーがまぁべつに（ex. 継承関係とか？違うかも
    - 2
        - interface value は 様々な具体値を格納できる
        - むしろ「集合」を値として扱える
        - type assertion使うと この中から型を明示的にみわけられる
        - switch case できる
        - 「具体型がインタフェースを満たしていること」が重要．
        - 実装詳細が隠されていること，がポイントではない
            - 別に一緒だって良いしね
        - 「集合を見分ける」ことがポイントぽいよ

- 前者: subtype polymorphism
- 後者: ad hoc polymorphism
- まぁおぼえなくてもいいよ（！？
    - 2つめのスタイルをおぼえておくのが重要らしい

- sql扱うAPI
    - SQL injectionできないように クエリと変数分離してるよ まぁとうぜんだね
    - validation部分が関係してくるのかな
    - クエリ中の '?' を 引数に変換してくれる
    - 引数は boolean / number / string / nil ..
    - ↑の引数を，SQL向けnotationに変換してから，'?'のいちに格納してくれる

- 各型にcastしながら if-else chain 噛ませることで switch case みたいなことできる
    - interfaceValue.(type) で型を取り出せるみたいだね
    - これぞ type switch!
    - （7.10にそんな記述はなかったと思うんだけどなぁ
    - （通常カッコ内の型にcastされるはず. ここでいう typeは特殊な扱いなのじゃろうか

- switch書くときは順序に気をつけような
    - goのswitchは 上位にmatchしたら下位はは評価されないからな( 1.8
    - かならずdefaultはつけろよ  fallthroughダメだよ

- caseの中でキャスト後の値にアクセスできるような書き方もできるよ
    - boolとかstringとかでひつようらしい フムー？
    - switch x := x.(type) { /* cases */}
        - この文脈において 同名再利用はよくあることらしい
        - because: swtch自体がscopeつくるからok

- なお上記書き方でcaseで複数型が並ぶ場合，interfeace{}型になるんだって

- type switch で 「集合 => 集合」　みたいな絞り方はできるのかな
    - 「Number（数） => Int（整数）」 じゃなくて「Number （数）=> Fraction（分数）」みたいな（例が妥当かは知らん
    - x.(type) は型を貸すっぽいから無理なのかなー
    - caseの比較が完全一致なのかどうか，だね
    - やってみろ案件か...時間があったらやる

- ちなsqlQuoteにおいては
    - 想定型ではない場合panicするらしいよ
    - 条件満たすものが渡される，という前提ぽい
    - まぁstringでもnilでもないものがプリペアドステートメントに渡されるのは想定外だよね

# 7.14

- 4.5でJSONのdecodeやったね
    - encoding/xmlもにたようなAPiあるよ
    - domツリー表現を構築するときには便利，だけどあんま使わないね

- 低レイヤーのtokenベースのapiがあるよ
    - encoding/xml の NewDecoder っぽい
    - inputをいい感じにtoken列を出力するよ
    - 4種類だって
        - StartElem: <name>
        - EndElem: </name>
        - CharData: <p>char data<p> のなかみ？
        - Comment: <!-- comment -->
    - とりあえずこれらはすべてTokenインタフェースをみたすと

- これが switch type の例として出てくるぽい
    - （traditional interface  : 実装詳細を隠して拡張性上げる
    - （descriminated union type : type switch で処理変える. 別に拡張したいわけではなさそう

- xmlselct : inputされた xml から os.Args[1:] のタグ名を含むやーつを表示する
    - stackされていった StartElem.Name と os.Args[1:] の比較
    - xmlをいったんパースして構造読み取ってからオペレーション，ではなく読み取りながら処理できるぞい，という点でうれしいっぽい

- Q: attrでもけんさくできるようにしようぜー
    - .class とか #id とかで指定できるように，ということ？
    - なんか面倒そうだなー..とおもったけどそうでもないや
    - 1点目
        - stack = []string だけど
        - stack = []Startelem とかにするとよさそう
    - 2点目
        - Args[1:] として渡される tagname / .classname / #idname の場合わけ(つらたん？
        - containsAllの処理をちょりっと変えるだけかなぁ

- Q: token based API つかって任意xmlを読み込みgeneric node のtreeをconstructせよ
    - data Node = CharData string | Element name attr Node （似非Haskell）においてツリー構造つくれやーみたいな話か
        - tour of go でツリー作ったのに似てるっちゃにてる？
    - 独自型定義したうえで，childnodeが L/Rではなくsliceになるくらい
    - 時間があればできそうだけど時間がない

