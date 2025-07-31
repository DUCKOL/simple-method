import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import sys
import random

# --- VLESS 配置参数 ---
USER_ID = '2e24b381-09e5-4386-b8c2-033c1bc40b12'
PORT = 443
PATH = '/?ed=2560'
# ==========================================================
# VVVVVVVV  这里是根据您的要求修改的地方  VVVVVVVV
REMARKS_PREFIX = '@DUCKOL(Github)'  # <-- 已将别名前缀修改为您指定的名称
# ^^^^^^^^  这里是根据您的要求修改的地方  ^^^^^^^^
# ==========================================================
OUTPUT_FILE = 'vless_links.txt'
DOMAINS_FILE = 'domains.txt'

# --- 目标URL列表，用于抓取IP ---
URLS_TO_SCRAPE = [
    'https://api.uouin.com/cloudflare.html', 
    'https://ip.164746.xyz'
]
IP_PATTERN = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def scrape_ips():
    """从目标URL抓取IP地址并返回一个去重后的列表"""
    unique_ips = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    print("🚀 开始抓取IP地址...")
    for url in URLS_TO_SCRAPE:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            ip_matches = re.findall(IP_PATTERN, response.text)
            if ip_matches:
                unique_ips.update(ip_matches)
        except requests.RequestException as e:
            print(f"    ❌ 访问URL {url} 失败: {e}")
            
    return list(unique_ips)

def read_domains():
    """从 domains.txt 读取域名列表 """
    try:
        with open(DOMAINS_FILE, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        return domains
    except FileNotFoundError:
        print(f"❌ 错误: 域名文件 '{DOMAINS_FILE}' 未找到。")
        return []

# --- 主程序 ---
if __name__ == "__main__":
    # 1. 抓取IP
    live_ips = scrape_ips()
    if not live_ips:
        print("❌ 未能抓取到任何IP地址，程序终止。")
        sys.exit(1)
    print(f"✨ 成功抓取到 {len(live_ips)} 个不重复的IP地址。")

    # 2. 读取伪装域名
    host_domains = read_domains()
    if not host_domains:
        print("❌ 域名文件为空或未找到，程序终止。")
        sys.exit(1)
    print(f"📂 成功读取到 {len(host_domains)} 个伪装域名。")
    
    # 3. 为每个IP生成VLESS链接
    all_vless_links = []
    print("\n🔧 开始为每个IP生成VLESS节点...")
    
    for ip in sorted(live_ips):
        address = ip
        random_host = random.choice(host_domains)
        
        # 使用新的前缀来格式化别名
        remarks = f"{REMARKS_PREFIX} IP[{address}] Host[{random_host}]"
        
        encoded_path = urllib.parse.quote(PATH)
        encoded_remarks = urllib.parse.quote(remarks)
        
        vless_link = (
            f"vless://{USER_ID}@{address}:{PORT}?"
            f"encryption=none&security=tls&type=ws&host={random_host}&path={encoded_path}"
            f"#{encoded_remarks}"
        )
        all_vless_links.append(vless_link)
        
    # 4. 将所有生成的链接写入文件
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_vless_links))
        print(f"\n✅ 成功！所有 {len(all_vless_links)} 条节点链接已写入到 '{OUTPUT_FILE}' 文件中。")
    except IOError as e:
        print(f"\n❌ 写入文件失败: {e}")
        sys.exit(1)
