-- 数値リストのリストから合計値(sum)の最も大きいリストを返す
-- 合計値が等しい場合は要素数が少ない方を返す
maximumList :: (Num a, Ord a) => [[a]] -> [a]
maximumList = foldl maxList [0]

-- ２つのリストを,そのsumで比較
-- max a b の list ver.
maxList :: (Num a, Ord a) => [a] -> [a] -> [a]
maxList as bs
    | sum as > sum bs   = as
    | sum as < sum bs   = bs
    | otherwise         = shortList as bs

-- 2つのリストのうち，短いものをreturn
shortList :: (Num a, Ord a) => [a] -> [a] -> [a]
shortList as bs
    | length as < length bs = as
    | otherwise             = bs

main = do
    print $ maxList [1,2,3] [1,4,2]
    print $ maximumList [[1,2,3],[1,4,2],[3,2,4],[1,2]]
