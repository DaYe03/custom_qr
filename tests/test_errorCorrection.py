import pytest
from qr_code.errorCorrection import ErrorCorrection

@pytest.fixture
def ec():
    return ErrorCorrection()

# def test_get_generator_poly(ec):
#     # Verifica il polinomio generatore per un grado specifico
#     degree = 3
#     expected_poly = [1, 5, 17, 49]  # Modifica questi valori con quelli attesi
#     result = ec.get_generator_poly(degree)
#     assert result == expected_poly, f"Expected {expected_poly}, but got {result}"

# def test_getEDC(ec):
#     data = [65, 166, 135, 71, 71, 7, 51, 162, 242, 247, 119, 119, 114, 231, 23, 38, 54, 246, 70, 82, 230, 54, 246, 210, 240, 236, 17, 236]  
#     codewords = 44
#     expected_remainder = [52, 61, 242, 187, 29, 7, 216, 249, 103, 87, 95, 69, 188, 134, 57, 20] 
    
#     result = ec.getEDC(data, codewords)
#     assert result == expected_remainder, f"Expected {expected_remainder}, but got {result}"

# def test_get_generator_poly_zero_degree(ec):
#     # Verifica il polinomio generatore per il grado zero
#     degree = 0
#     expected_poly = [1]  # Modifica con il valore atteso
#     result = ec.get_generator_poly(degree)
#     assert result == expected_poly, f"Expected {expected_poly}, but got {result}"

# def test_getEDC_edge_case(ec):
#     # Test edge case con dati e codeword minimi
#     data = [0]  # Modifica con dati di edge case se necessario
#     codewords = 1
#     expected_remainder = [0]  # Modifica con il risultato atteso
    
#     result = ec.getEDC(data, codewords)
#     assert result == expected_remainder, f"Expected {expected_remainder}, but got {result}"
