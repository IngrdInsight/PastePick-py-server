from fastapi.testclient import TestClient
from main import app
from typing import Dict, Any

client = TestClient(app)

# filename -> expected toothpaste_id (0 means "not in database")
test_1_initial = {
    "apteq_0.png": 3,
    "apteq_1.jpeg": 3,
    "apteq_2.jpeg": 3,
    "apteq_3.jpeg": 3,
    "apteq_4.jpeg": 3,
    "apteq_5.jpeg": 3,
    "apteq_6.jpeg": 3,
    "apteq_7.jpeg": 3,
    "apteq_8.jpg": 3,
    "apteq_9.jpg": 3,
    "be_confident.jpg": 0,
    "biotene.png": 0, # Not in existing set
    "colgate_0.png": 2,
    "drjen_0.png": 0, # Not in existing set
    "drjen_1.webp": 0, # Not in existing set
    "elmex_0.png": 4,
    "elmex_1.jpg": 4,
    "gum_bio.webp": 0,
    "oxygenol_0.jpg": 0,
    "pronamel_0.png": 0, # Not in existing set (Sensodyne/Pronamel is 5)
    "pronamel_1.png": 0, # Not in existing set
    "pronamel_2.png": 0, # Not in existing set
    "pronamel_3.png": 0, # Not in existing set
    "pronamel_4.png": 0, # Not in existing set
    "pronamel_5.png": 0, # Not in existing set
    "yotuel_0.jpg": 0, # Not in existing set
    "yotuel_1.webp": 0, # Not in existing set
}
test_2_second = {
    "apteq_0.png": 3,
    "apteq_1.jpeg": 3,
    "apteq_2.jpeg": 3,
    "apteq_3.jpeg": 3,
    "apteq_4.jpeg": 3,
    "apteq_5.jpeg": 3,
    "apteq_6.jpeg": 3,
    "apteq_7.jpeg": 3,
    "apteq_8.jpg": 3,
    "apteq_9.jpg": 3,
    "be_confident.jpg": 0,
    "biotene.png": 6, # Now in existing set
    "colgate_0.png": 2,
    "drjen_0.png": 0, # Not in existing set
    "drjen_1.webp": 0, # Not in existing set
    "elmex_0.png": 4,
    "elmex_1.jpg": 4,
    "gum_bio.webp": 0,
    "oxygenol_0.jpg": 0,
    "pronamel_0.png": 5, # Now in existing set (Sensodyne/Pronamel is 5)
    "pronamel_1.png": 5,
    "pronamel_2.png": 5,
    "pronamel_3.png": 5,
    "pronamel_4.png": 5,
    "pronamel_5.png": 5,
    "yotuel_0.jpg": 0, # Not in existing set
    "yotuel_1.webp": 0, # Not in existing set
}
test_3_third = {
    "apteq_0.png": 3,
    "apteq_1.jpeg": 3,
    "apteq_2.jpeg": 3,
    "apteq_3.jpeg": 3,
    "apteq_4.jpeg": 3,
    "apteq_5.jpeg": 3,
    "apteq_6.jpeg": 3,
    "apteq_7.jpeg": 3,
    "apteq_8.jpg": 3,
    "apteq_9.jpg": 3,
    "be_confident.jpg": 0,
    "biotene.png": 6,
    "colgate_0.png": 2,
    "drjen_0.png": 7, # Now in existing set
    "drjen_1.webp": 7, # Now in existing set
    "elmex_0.png": 4,
    "elmex_1.jpg": 4,
    "gum_bio.webp": 0,
    "oxygenol_0.jpg": 0,
    "pronamel_0.png": 5,
    "pronamel_1.png": 5,
    "pronamel_2.png": 5,
    "pronamel_3.png": 5,
    "pronamel_4.png": 5,
    "pronamel_5.png": 5,
    "yotuel_0.jpg": 8, # Now in existing set
    "yotuel_1.webp": 8, # Now in existing set
}

images_path = "./toothpastes/"
results: Dict[str, Any] = {
    "matches_existing": {"count": 0, "total_similarity": 0.0},
    "misses_false_positive": {"count": 0, "total_similarity": 0.0},
    "misses_wrong_brand": {"count": 0, "total_similarity": 0.0},
    "matches_not_existing": 0,
    "misses_false_negative": 0,
    "errors": 0,
    "total": 0,
}

def get_mime_type(filename: str) -> str:
    """Determine MIME type based on file extension."""
    ext = filename.lower().split('.')[-1]
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
    }
    return mime_types.get(ext, 'image/jpeg')


def test_image_processing(test_suite: Dict[str, int]):
    """Process all images in test suite and track results."""
    for filename, expected_match in test_suite.items():
        try:
            file_path = f"{images_path}{filename}"
            with open(file_path, 'rb') as f:
                response = client.post(
                    "/api/search-by-image",
                    files={'file': (filename, f, get_mime_type(filename))},
                )

                print(f"Response for {filename}: {response.status_code} - {response.json()}")

                if response.status_code == 200:
                    response_data = response.json()

                    if 'results' in response_data and len(response_data['results']) > 0:
                        top_result = response_data['results'][0]
                        returned_id = top_result.get("id")
                        similarity = top_result.get("similarity", 0.0)

                        # Case 1: API returned None/null (not in database)
                        if returned_id is None:
                            if expected_match == 0:
                                results["matches_not_existing"] += 1
                            else:
                                results["misses_false_negative"] += 1

                        # Case 2: API returned an ID (found in database)
                        else:
                            if returned_id == expected_match and expected_match != 0:
                                results["matches_existing"]["count"] += 1
                                results["matches_existing"]["total_similarity"] += similarity
                            elif expected_match == 0:
                                results["misses_false_positive"]["count"] += 1
                                results["misses_false_positive"]["total_similarity"] += similarity
                            elif returned_id != expected_match and expected_match != 0:
                                results["misses_wrong_brand"]["count"] += 1
                                results["misses_wrong_brand"]["total_similarity"] += similarity

                        results["total"] += 1
                    else:
                        print(f"Warning: No results returned for {filename}")
                        results["total"] += 1
                else:
                    print(f"Error: Got status code {response.status_code} for {filename}")
                    results["errors"] += 1
                    results["total"] += 1

        except FileNotFoundError:
            results["errors"] += 1
            results["total"] += 1
            print(f"Error: File not found {filename}")
        except Exception as e:
            results["errors"] += 1
            results["total"] += 1
            print(f"Error processing {filename}: {e}")


def test_analysis():
    print("\n" + "=" * 60)
    print("TEST RESULTS ANALYSIS")
    print("=" * 60)

    # Matches (existing brands)
    if results["matches_existing"]["count"] > 0:
        avg_similarity = results["matches_existing"]["total_similarity"] / results["matches_existing"]["count"]
        print(f"\n✓ Matches (existing brands):")
        print(f"  Count: {results['matches_existing']['count']}")
        print(f"  Avg Similarity: {avg_similarity:.2f}")
    else:
        print(f"\n✓ Matches (existing brands): 0")

    # Matches (not existing)
    print(f"\n✓ Matches (not in database):")
    print(f"  Count: {results['matches_not_existing']}")

    # Misses - False Positives
    if results["misses_false_positive"]["count"] > 0:
        avg_similarity = results["misses_false_positive"]["total_similarity"] / results["misses_false_positive"][
            "count"]
        print(f"\n✗ False Positives (matched existing, should be not-existing):")
        print(f"  Count: {results['misses_false_positive']['count']}")
        print(f"  Avg Similarity: {avg_similarity:.2f}")
    else:
        print(f"\n✗ False Positives: 0")

    # Misses - False Negatives
    print(f"\n✗ False Negatives (not matched, should be existing):")
    print(f"  Count: {results['misses_false_negative']}")

    # Misses - Wrong Brand
    if results["misses_wrong_brand"]["count"] > 0:
        avg_similarity = results["misses_wrong_brand"]["total_similarity"] / results["misses_wrong_brand"]["count"]
        print(f"\n✗ Wrong Brand Matches:")
        print(f"  Count: {results['misses_wrong_brand']['count']}")
        print(f"  Avg Similarity: {avg_similarity:.2f}")
    else:
        print(f"\n✗ Wrong Brand Matches: 0")

    # Summary
    print("\n" + "=" * 60)
    total_correct = results["matches_existing"]["count"] + results["matches_not_existing"]
    if results["total"] > 0:
        accuracy = (total_correct / results["total"]) * 100
        print(f"Total Accuracy: {accuracy:.1f}% ({total_correct}/{results['total']})")

    print(f"Errors: {results['errors']}")
    print(f"Total Tests: {results['total']}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print("Starting image processing tests...")
    test_image_processing(test_3_third)
    test_analysis()
