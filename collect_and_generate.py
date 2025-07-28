import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import sys

# --- VLESS 链接的核心配置参数 ---
USER_ID = '2e24b381-09e5-4386-b8c2-033c1bc40b12'
PORT = 443
HOST = 'ysun74.ysunyang.qzz.io'
PATH = '/?ed=2560'
REMARKS_PREFIX = '@ys==>unlock all'
OUTPUT_FILE = 'vless_links.txt' # 最终输出的文件名

# --- 用于抓取 IP 的目标网址列表 ---
URLS_TO_SCRAPE = [
    'https://api.uouin.com/cloudflare.html', 
    'https://ip.164746.xyz'
]

# 用于从文本中匹配 IP 地址的正则表达式
IP_PATTERN = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def scrape_live_ips():
    """
    从所有目标 URL 抓取 IP 地址。
    返回一个去重后的 IP 地址集合。
    """
    unique_ips = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("🚀 开始从以下 URL 抓取实时 IP 地址:")
    for url in URLS_TO_SCRAPE:
        print(f"  - 正在访问: {url}")
        try:
            # 发起网络请求，设置10秒超时
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # 如果请求状态码不是 2xx，则抛出异常

            # 使用 BeautifulSoup 解析 HTML 内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 使用正则表达式查找所有符合格式的 IP 地址
            ip_matches = re.findall(IP_PATTERN, soup.get_text())
            
            if ip_matches:
                unique_ips.update(ip_matches)
                print(f"    ✅ 在此 URL 找到 {len(ip_matches)} 个 IP 地址。")
            else:
                print(f"    ⚠️ 在此 URL 未找到任何 IP 地址。")

        except requests.RequestException as e:
            print(f"    ❌ 访问 URL 失败: {e}")
            
    return unique_ips

def generate_vless_links(ip_set):
    """
    根据提供的 IP 地址集合，生成 VLESS 链接列表。
    """
    all_vless_links = []
    print("\n🔧 开始为每个唯一的 IP 地址生成 VLESS 链接...")

    # 对 IP 进行排序，以确保每次生成的文件内容顺序一致
    for ip in sorted(list(ip_set)): 
        # address 部分直接使用抓取到的 IP
        address = ip
        
        # 创建符合格式的别名: @ys==>unlock all [IP地址]
        remarks = f"{REMARKS_PREFIX} {ip}"
        
        # 为了 URL 安全，对路径和别名中的特殊字符进行编码
        encoded_path = urllib.parse.quote(PATH)
        encoded_remarks = urllib.parse.quote(remarks)
        
        # 按照 VLESS 格式拼接完整的链接字符串
        vless_link = (
            f"vless://{USER_ID}@{address}:{PORT}?"
            f"encryption=none&security=tls&type=ws&host={HOST}&path={encoded_path}"
            f"#{encoded_remarks}"
        )
        all_vless_links.append(vless_link)
        
    return all_vless_links

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 执行 IP 抓取
    scraped_ips = scrape_live_ips()
    
    if not scraped_ips:
        print("\n❌ 未能抓取到任何有效的 IP 地址，程序终止。")
        sys.exit(1) # 退出并返回错误码，GitHub Actions 会将此次运行标记为失败
        
    print(f"\n✨ 抓取完成！共找到 {len(scraped_ips)} 个不重复的 IP 地址。")
    
    # 2. 根据抓取到的 IP 生成链接
    vless_links = generate_vless_links(scraped_ips)
    
    # 3. 将所有生成的链接写入文件
    # 使用 'w' 模式写入，这意味着每次运行时都会清空并重写文件，达到覆盖效果。
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # 使用换行符 '\n' 将列表中的每个链接连接成一个长字符串后写入文件
            f.write('\n'.join(vless_links))
        print(f"\n✅ 成功！所有 {len(vless_links)} 条链接已覆盖写入到 '{OUTPUT_FILE}' 文件中。")
    except IOError as e:
        print(f"\n❌ 写入文件失败: {e}")
        sys.exit(1) # 写入失败则终止程序
