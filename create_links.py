import urllib.parse
import sys

# --- VLESS 链接的核心配置参数 ---
USER_ID = '2e24b381-09e5-4386-b8c2-033c1bc40b12'
PORT = 443
PATH = '/?ed=2560'
REMARKS_PREFIX = '@ys==>unlock all'

# --- 输入和输出文件名 ---
DOMAINS_FILE = 'domains.txt'
OUTPUT_FILE = 'vless_links.txt'

def read_first_domain():
    """从 domains.txt 文件读取第一个有效的域名。"""
    print(f"📄 正在从 '{DOMAINS_FILE}' 文件中寻找域名...")
    try:
        with open(DOMAINS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith('#'):
                    print(f"    ✅ 找到第一个可用域名: {domain}")
                    return domain
        print(f"    ⚠️ 在 '{DOMAINS_FILE}' 中未找到任何有效的域名。")
        return None
    except FileNotFoundError:
        print(f"    ❌ 致命错误: 找不到源文件 '{DOMAINS_FILE}'！")
        return None

def generate_vless_link(domain):
    """为单个域名生成 VLESS 链接。"""
    print(f"\n🔧 正在为域名 '{domain}' 创建链接...")
    address = domain
    host = domain
    remarks = f"{REMARKS_PREFIX} {domain}"
    
    encoded_path = urllib.parse.quote(PATH)
    encoded_remarks = urllib.parse.quote(remarks)
    
    vless_link = (
        f"vless://{USER_ID}@{address}:{PORT}?"
        f"encryption=none&security=tls&sni={host}&type=ws&host={host}&path={encoded_path}"
        f"#{encoded_remarks}"
    )
    return vless_link

if __name__ == "__main__":
    domain_to_use = read_first_domain()
    
    if not domain_to_use:
        print("\n❌ 程序因缺少域名而终止。")
        sys.exit(1)
    
    final_link = generate_vless_link(domain_to_use)
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(final_link)
        print(f"\n✅ 操作成功！新的链接已覆盖写入到 '{OUTPUT_FILE}'。")
    except IOError as e:
        print(f"\n❌ 写入文件时发生错误: {e}")
        sys.exit(1)
