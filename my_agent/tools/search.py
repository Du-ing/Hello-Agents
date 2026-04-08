import requests
import os

def baidu_search(query: str) -> str:
    api_key = os.getenv("BAIDU_SEARCH_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 BAIDU_SEARCH_API_KEY")

    url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": query}],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web","top_k": 10}],
        # "search_recency_filter": "year"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    if "references" not in data or not data["references"]:
        return "未找到相关搜索结果"
    
    # 取data["references"]前三个结果的content
    res = [f"[{idx + 1}] {ref['content']}" for idx, ref in enumerate(data["references"][:3])]
    answer = "\n".join(res)
    return answer

if __name__ == "__main__":
    result = baidu_search("Python编程")
    print("🤖 搜索结果：", result)
    print("\n📚 搜索结果：")