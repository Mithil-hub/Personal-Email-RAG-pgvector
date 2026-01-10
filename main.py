# main.py
import time
from src.rag.pipeline import retrieve_relevant_chunks
from src.rag.llm_handler import answer_query

def main():
    user_id = input("Enter your user_id (default: user_1): ").strip() or "user_1"
    
    print("\n=== Personal Email RAG System ===")
    print("Ask questions about your emails. Type 'exit' to quit.\n")
    
    while True:
        query = input("Your question: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not query:
            continue
        
        try:
            # Track metrics
            start_time = time.time()
            
            retrieval_start = time.time()
            snippets = retrieve_relevant_chunks(query, user_id=user_id, k=3)
            retrieval_time = time.time() - retrieval_start
            
            if not snippets:
                print("\n⚠️  No relevant emails found for your query.\n")
                continue
            
            generation_start = time.time()
            answer = answer_query(query, snippets)
            generation_time = time.time() - generation_start
            
            total_time = time.time() - start_time
            
            # Display results
            print(f"\n{answer}\n")
            print(f"[Metrics] Retrieval: {retrieval_time:.2f}s | Generation: {generation_time:.2f}s | Total: {total_time:.2f}s\n")
        
        except ValueError as e:
            print(f"\n❌ Security Error: {e}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
