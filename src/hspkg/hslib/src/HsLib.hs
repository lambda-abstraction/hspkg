{-# LANGUAGE ForeignFunctionInterface, BangPatterns #-}

module HsLib where

import Foreign (Ptr, nullPtr)
import Foreign.C (CULong(..), CInt(..))
import Foreign.C.String (CString, withCString)

newtype PyObject = PyObject (Ptr ())

foreign import ccall unsafe "cbits.h PyLong_AsUnsignedLong" _PyLong_AsUnsignedLong :: PyObject -> IO CULong
foreign import ccall unsafe "cbits.h PyLong_FromString" _PyLong_FromString :: CString -> Ptr CString -> CInt -> IO PyObject

fib :: (Ord n, Num n, Num r) => n -> r
fib !n = go n 0 1 where
    go !n !a !b
        | n > 0 = go (n - 1) b (a + b)
        | otherwise = a

hs_fib :: PyObject -> PyObject -> IO PyObject
hs_fib _ !n = do
    hs_res :: Integer <- fib <$> _PyLong_AsUnsignedLong n
    withCString (show hs_res) $ \c_str -> _PyLong_FromString c_str nullPtr 10

foreign export ccall hs_fib :: PyObject -> PyObject -> IO PyObject