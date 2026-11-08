import unittest
from calculator import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)                  
        self.assertEqual(add(5, -3), 2)                
        self.assertEqual(add(0, 0), 0)                  

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)

    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(5, 0), 0)             

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)              
        self.assertAlmostEqual(divide(1, 3), 0.3333333, places=5) 
        
        
        with self.assertRaises(ValueError):
            divide(1, 0)
        
        
        with self.assertRaises(ValueError) as ctx:
            divide(5, 0)
        self.assertIn("zero", str(ctx.exception))

    def test_type_error(self):
       
        with self.assertRaises(TypeError):
            add("2", 3)
        with self.assertRaises(TypeError):
            divide(10, "2")

if __name__ == "__main__":
    unittest.main()


# --- FAIL TEST z zadania 2: celowe popsucie testu -------
# zmiana: w calculator.py w funkcji add zmieniono "return a + b" na "return a - b"
# outcome: test zwrocil FAIL AssertionError: -1 != 5 (oczekiwano 5 otrzymano -1)
# naprawa: przywrocono "return a + b" testy powróciły do stanu OK