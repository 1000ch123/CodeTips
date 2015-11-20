powers :: Int -> [Int]
powers n = map (n^) [0..]

step :: [Int] -> Int -> [Int]
step [] _ = []
step (x:xs) t
    | x <= t     = x: step xs (t - x)
    | otherwise  = step xs t

power_expansion :: Int -> [Int]
power_expansion n = step source n
    where
        source = reverse . takeWhile (<n) $ powers 2

main = do
    print $ power_expansion 50
