import json
from nlp_detector import FakeNewsDetector
from deepfake_detector import DeepfakeDetector

def test_nlp_module():
    print("--> Testing Fake News NLP Module...")
    detector = FakeNewsDetector()

    with open("samples/sample_articles.json", "r") as f:
        data = json.load(f)

    for item in data["test_cases"]:
        res = detector.analyze_text(item["body"])
        print(f"[{item['id']}] Expected: {item['category']} => Got: {res['verdict']} ({res['confidence']}%)")
        assert res["verdict"] in ("Real", "Fake"), "Verdict should be Real or Fake"
        assert "confidence" in res
        assert "explanation" in res

    # Test empty string error handling
    empty_res = detector.analyze_text("   ")
    assert "error" in empty_res, "Should handle empty text gracefully"
    print("NLP Module tests PASSED successfully!\n")

def test_deepfake_module():
    print("--> Testing Deepfake Image Forensic Module...")
    detector = DeepfakeDetector()

    for sample_name in ["authentic_sample.jpg", "manipulated_sample.jpg", "synthetic_sample.jpg"]:
        path = f"samples/{sample_name}"
        with open(path, "rb") as f:
            bytes_data = f.read()
        res = detector.analyze_image(bytes_data, sample_name)
        print(f"[{sample_name}] => Verdict: {res['verdict']} | Authenticity: {res['authenticity_score']}/100 | ELA: {res['ela_score']}")
        assert "verdict" in res
        assert "authenticity_score" in res
        assert "indicators" in res
        assert "ela_image" in res

    # Test invalid byte input error handling
    invalid_res = detector.analyze_image(b"not an image", "corrupt.jpg")
    assert "error" in invalid_res, "Should handle corrupt file format gracefully"
    print("Deepfake Module tests PASSED successfully!\n")

if __name__ == "__main__":
    test_nlp_module()
    test_deepfake_module()
    print("ALL UNIT TESTS PASSED!")
