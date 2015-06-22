-- CTO Lv2
data Size = M | L
    deriving (Eq, Show)

data PizzaName = Genovase | Margherita
    deriving (Eq, Show)

data SideName = Potato | Green | Ceaser
    deriving (Eq, Show)

data Menu = Pizza PizzaName Size | Side SideName
    deriving (Eq, Show)

type Price = Int

price :: Menu -> Int
price (Pizza name size)
    | name == Genovase && size == M = 1000
    | name == Genovase && size == L = 1500
    | name == Margherita && size == M = 1300
    | name == Margherita && size == L = 1800
    | otherwise = 0
price (Side name)
    | name == Potato = 400
    | name == Green = 500
    | name == Ceaser = 600
    | otherwise = 0

sumPrice :: [Menu] -> Int
sumPrice = sum . map price

myMenu :: [Menu]
myMenu = [
    (Pizza Genovase M),
    (Side Potato),
    (Side Green)
    ]

hasPizza :: [Menu] -> Bool
hasPizza = any func
    where func (Pizza _ _ ) = True
          func _            = False


main = do
    print $ price (Pizza Genovase M)
    print $ sumPrice myMenu
    print $ hasPizza myMenu
