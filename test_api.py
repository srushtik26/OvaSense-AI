"""
Simple test script to verify the API is working
Run this after starting the backend server
"""

import requests
import json

# Test data
test_assessment = {
    "age": 25,
    "height_cm": 165,
    "weight_kg": 70,
    "family_history_pcos": False,
    "cycle_length_avg": 35,
    "cycles_last_12_months": 8,
    "missed_period_frequency": 4,
    "period_flow_type": "normal",
    "acne_severity": 3,
    "facial_hair_growth": 2,
    "hair_thinning": 1,
    "dark_patches_skin": False,
    "sudden_weight_gain": True,
    "fatigue_level": 4,
    "sugar_cravings": 4,
    "stress_level": 7,
    "sleep_hours": 6.5,
    "exercise_days_per_week": 2,
    "diet_type": "vegetarian"
}

def test_assessment_api():
    """Test the assessment analyze endpoint"""
    print("Testing OvaSense AI API...")
    print("=" * 50)
    
    try:
        # Test health endpoint
        print("\n1. Testing health endpoint...")
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
        
        # Test assessment endpoint
        print("\n2. Testing assessment endpoint...")
        response = requests.post(
            "http://localhost:8000/api/v1/assessments/analyze",
            json=test_assessment
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Assessment successful!")
            print("\nResults:")
            print(f"  Risk Level: {result.get('risk_level')}")
            print(f"  Phenotype: {result.get('phenotype')}")
            print(f"  Confidence: {result.get('confidence')}")
            print(f"  Risk Score: {result.get('risk_score')}%")
            print(f"\n  Key Drivers: {', '.join(result.get('key_drivers', [])[:3])}")
            print(f"\n  Assessment ID: {result.get('assessment_id')}")
            
            # Test getting the assessment
            if result.get('assessment_id'):
                print("\n3. Testing get assessment endpoint...")
                assessment_id = result['assessment_id']
                get_response = requests.get(
                    f"http://localhost:8000/api/v1/assessments/{assessment_id}"
                )
                if get_response.status_code == 200:
                    print("✅ Retrieved assessment successfully")
                else:
                    print(f"❌ Failed to retrieve assessment: {get_response.status_code}")
            
            print("\n" + "=" * 50)
            print("✅ All tests passed!")
            return True
        else:
            print(f"❌ Assessment failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        print("   Start the server with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_assessment_api()

