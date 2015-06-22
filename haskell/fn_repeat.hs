-- 「関数を指定回数適用する」関数
-- 高階関数の何かでありそうなんだが

fnRepeat :: (a -> a) -> Int -> a -> a
fnRepeat f 0 = id
fnRepeat f n = f . fnRepeat f (n-1)

fnRepeatFold :: (a -> a) -> Int -> a -> a
fnRepeatFold fn n init = foldr (\_ acc -> fn acc) init [1..n]

fnRepeatIterate :: (a->a) -> Int -> a -> a
fnRepeatIterate fn n x = last . take (n+1) $ iterate fn x

main = do
    print $ fnRepeat (^2) 3 2
    print $ fnRepeatFold (^2) 3 2
    print $ fnRepeatIterate (^2) 3 2
