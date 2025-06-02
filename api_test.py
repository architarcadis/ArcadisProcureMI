#!/usr/bin/env python3
"""
API Connection Test for Market Intelligence
Tests Google Search API and OpenAI API connectivity
"""

import os
import requests
from googleapiclient.discovery import build

def test_google_search_api():
    """Test Google Custom Search API"""
    try:
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        google_cse_id = os.environ.get("GOOGLE_CSE_ID")
        
        if not google_api_key or not google_cse_id:
            print("❌ Google API credentials missing")
            return False
            
        service = build("customsearch", "v1", developerKey=google_api_key)
        
        # Test search
        result = service.cse().list(
            q="Microsoft financial performance",
            cx=google_cse_id,
            num=3
        ).execute()
        
        if 'items' in result and len(result['items']) > 0:
            print(f"✅ Google Search API working - Found {len(result['items'])} results")
            print(f"   Sample result: {result['items'][0]['title'][:50]}...")
            return True
        else:
            print("❌ Google Search API - No results returned")
            return False
            
    except Exception as e:
        print(f"❌ Google Search API error: {str(e)}")
        return False

def test_openai_api():
    """Test OpenAI API"""
    try:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_api_key:
            print("❌ OpenAI API key missing")
            return False
            
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Test message - respond with 'API working'"}],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ OpenAI API working - Response: {message}")
            return True
        else:
            print(f"❌ OpenAI API error - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return False

def test_market_intelligence_query():
    """Test a realistic market intelligence query"""
    try:
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        google_cse_id = os.environ.get("GOOGLE_CSE_ID")
        
        if not google_api_key or not google_cse_id:
            return False
            
        service = build("customsearch", "v1", developerKey=google_api_key)
        
        # Test query similar to what market intelligence uses
        test_queries = [
            '"Microsoft" financial performance earnings revenue',
            '"Google" innovation product launch',
            '"Amazon" regulatory compliance'
        ]
        
        total_results = 0
        for query in test_queries:
            try:
                result = service.cse().list(
                    q=query,
                    cx=google_cse_id,
                    num=5,
                    sort='date',
                    dateRestrict='m6'
                ).execute()
                
                if 'items' in result:
                    count = len(result['items'])
                    total_results += count
                    print(f"   Query '{query[:30]}...' - {count} results")
                else:
                    print(f"   Query '{query[:30]}...' - 0 results")
                    
            except Exception as e:
                print(f"   Query failed: {str(e)}")
        
        print(f"✅ Total market intelligence results: {total_results}")
        return total_results > 0
        
    except Exception as e:
        print(f"❌ Market intelligence test error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Testing API Connections for Market Intelligence")
    print("=" * 50)
    
    google_ok = test_google_search_api()
    openai_ok = test_openai_api()
    
    print("\n🎯 Testing Market Intelligence Queries")
    print("=" * 50)
    intelligence_ok = test_market_intelligence_query()
    
    print("\n📊 Summary")
    print("=" * 50)
    print(f"Google Search API: {'✅' if google_ok else '❌'}")
    print(f"OpenAI API: {'✅' if openai_ok else '❌'}")
    print(f"Market Intelligence: {'✅' if intelligence_ok else '❌'}")
    
    if not (google_ok and openai_ok):
        print("\n⚠️  API configuration issues detected.")
        print("   This explains why only 1 alert was generated.")
        print("   Please check your API keys and try again.")
    else:
        print("\n✅ All APIs working - investigating other causes...")