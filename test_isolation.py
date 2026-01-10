# test_isolation.py
"""
Multi-user isolation test script.
Tests that User A's queries while logged in as User B return zero results.
"""
from src.rag.pipeline import retrieve_relevant_chunks
from src.indexing.embedder import OllamaEmbeddings

def test_isolation():
    print("="*60)
    print("MULTI-USER ISOLATION TEST")
    print("="*60)
    
    # Test 1: User_1 queries their own data
    print("\n[Test 1] User_1 queries their own data (Spring 2026)")
    try:
        results = retrieve_relevant_chunks(
            query="Spring 2026 reduced course load",
            user_id="user_1",
            k=3
        )
        print(f"✅ PASS: Retrieved {len(results)} results for user_1")
        if results:
            print(f"   Sample: {results[0][3]}")  # subject
    except Exception as e:
        print(f"❌ FAIL: {e}")
    
    # Test 2: User_2 queries their own data
    print("\n[Test 2] User_2 queries their own data (Monday meeting)")
    try:
        results = retrieve_relevant_chunks(
            query="Monday team meeting Conference Room",
            user_id="user_2",
            k=3
        )
        print(f"✅ PASS: Retrieved {len(results)} results for user_2")
        if results:
            print(f"   Sample: {results[0][3]}")  # subject
    except Exception as e:
        print(f"❌ FAIL: {e}")
    
    # Test 3: SECURITY - User_2 tries to access User_1's data
    print("\n[Test 3] SECURITY: User_2 tries to access User_1's Spring 2026 data")
    try:
        results = retrieve_relevant_chunks(
            query="Spring 2026 reduced course load",
            user_id="user_2",  # Different user
            k=3
        )
        if len(results) == 0:
            print(f"✅ PASS: Isolation working - user_2 got 0 results (cannot see user_1's data)")
        else:
            print(f"❌ FAIL: Isolation broken - user_2 retrieved {len(results)} results from user_1!")
    except Exception as e:
        print(f"❌ FAIL: {e}")
    
    # Test 4: SECURITY - User_1 tries to access User_2's data
    print("\n[Test 4] SECURITY: User_1 tries to access User_2's meeting data")
    try:
        results = retrieve_relevant_chunks(
            query="Monday team meeting Conference Room",
            user_id="user_1",  # Different user
            k=3
        )
        if len(results) == 0:
            print(f"✅ PASS: Isolation working - user_1 got 0 results (cannot see user_2's data)")
        else:
            print(f"❌ FAIL: Isolation broken - user_1 retrieved {len(results)} results from user_2!")
    except Exception as e:
        print(f"❌ FAIL: {e}")
    
    # Test 5: Invalid user_id
    print("\n[Test 5] SECURITY: Empty user_id should raise error")
    try:
        results = retrieve_relevant_chunks(
            query="any query",
            user_id="",  # Empty
            k=3
        )
        print(f"❌ FAIL: Empty user_id did not raise error")
    except ValueError as e:
        print(f"✅ PASS: Empty user_id rejected - {e}")
    except Exception as e:
        print(f"⚠️  PARTIAL: Got error but wrong type - {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_isolation()
