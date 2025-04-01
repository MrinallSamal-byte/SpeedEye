from backend.ai_service import predict_speeding

def test_ai():
    assert predict_speeding(90) == 1  # Speeding
    assert predict_speeding(50) == 0  # Normal
    print("AI Model Test Passed!")

if __name__ == "__main__":
    test_ai()
