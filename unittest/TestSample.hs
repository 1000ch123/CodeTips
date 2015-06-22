module TestSample where


-- | addThree : add 3 to input val
-- >>> addThree 4
-- 7
-- >>> addThree 3
-- 6
-- >>> addThree 0
-- 3
--
-- prop> addThree x == x + 3

addThree :: Int -> Int
addThree x
    | x < 100 = x+3
    | otherwise = x+2

