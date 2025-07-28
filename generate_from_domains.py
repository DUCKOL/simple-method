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
    """
    从 domains.txt 文件读取第一个有效的域名。
    会自动忽略空白行和注释。
    """
    print(f"📄 开始从 '{DOMAINS_FILE}' 文件读取域名...")
    try:
        with open(DOMAINS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                # 如果行不为空且不是注释，则视为有效域名并立即返回
                if domain and not domain.startswith('#'):
                    print(f"    ✅ 成功读取到第一个有效域名: {domain}")
                    return domain
        
        # 如果循环结束都没有找到有效域名
        print(f"    ⚠️ 文件 '{DOMAINS_FILE}' 中未找到任何有效的域名。")
        return None
        
    except FileNotFoundError:
        print(f"    ❌ 错误：找不到域名文件 '{DOMAINS_FILE}'！")
        return None
    except Exception as e:
        print(f"    ❌ 读取文件时发生未知错误: {e}")
        return None

def generate_single_vless_link(domain):
    """
    根据提供的单个域名，生成 VLESS 链接。
    """
    print("\n🔧 开始为域名生成唯一的 VLESS 链接...")
    
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

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 读取第一个域名
    first_domain = read_first_domain()
    
    # 如果没有找到域名，则终止程序
    if not first_domain:
        print("\n❌ 因无法获取域名，程序终止。")
        sys.exit(1)
    
    # 2. 生成唯一的链接
    vless_link = generate_single_vless_link(first_domain)
    
    # 3. 将这条链接写入文件（'w' 模式会覆盖旧文件）
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(vless_link)
        print(f"\n✅ 成功！新生成的单条链接已覆盖写入到 '{OUTPUT_FILE}' 文件中。")
    except IOError as e:
        print(f"\n❌ 写入文件失败: {e}")
        sys.exit(1)
