import Test.HUnit
import System.IO

fact 1 = 1
fact n = n * fact (n - 1)

tests = TestList
    [ "fact 1" ~: fact 1 ~?= 1
    , "fact 2" ~: fact 2 ~?= 2
    , "fact 3" ~: fact 3 ~?= 6
    , "fact 4" ~: fact 4 ~?= 24
    , "fact 5" ~: fact 5 ~?= 120
    ]

main = do
    {-runTestText (putTextToHandle stderr False) tests-}
    runTestTT tests
