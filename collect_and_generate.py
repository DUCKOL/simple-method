import urllib.parse
import sys

# --- VLESS 链接的核心配置参数 (保持不变) ---
USER_ID = '2e24b381-09e5-4386-b8c2-033c1bc40b12'
PORT = 443
PATH = '/?ed=2560'
REMARKS_PREFIX = '@ys==>unlock all'

# --- 输入和输出文件名 ---
DOMAINS_FILE = 'domains.txt'  # 从这个文件读取域名
OUTPUT_FILE = 'vless_links.txt' # 最终输出的文件名

def read_domains():
    """
    从 domains.txt 文件读取域名列表。
    会自动去除空白行和行首尾的空格，并处理重复的域名。
    """
    print(f"📄 开始从 '{DOMAINS_FILE}' 文件读取域名...")
    try:
        with open(DOMAINS_FILE, 'r', encoding='utf-8') as f:
            # 读取所有行，去除每行的空格，并过滤掉空行
            domains = {line.strip() for line in f if line.strip()}
        
        if not domains:
            print(f"    ⚠️ 文件 '{DOMAINS_FILE}' 为空或不包含有效域名。")
            return set()
            
        print(f"    ✅ 成功读取到 {len(domains)} 个不重复的域名。")
        return domains
        
    except FileNotFoundError:
        print(f"    ❌ 错误：找不到域名文件 '{DOMAINS_FILE}'！请确保该文件存在于仓库中。")
        return None
    except Exception as e:
        print(f"    ❌ 读取文件时发生未知错误: {e}")
        return None

def generate_vless_links(domain_set):
    """
    根据提供的域名集合，为每个域名生成一个 VLESS 链接。
    """
    all_vless_links = []
    print("\n🔧 开始为每个域名生成 VLESS 链接...")

    # 对域名进行排序，以确保每次生成的文件内容顺序一致
    for domain in sorted(list(domain_set)):
        # 在这种模式下，address 和 host 都使用域名
        address = domain
        host = domain
        
        # 创建符合格式的别名: @ys==>unlock all [域名]
        remarks = f"{REMARKS_PREFIX} {domain}"
        
        # 为了 URL 安全，对路径和别名中的特殊字符进行编码
        encoded_path = urllib.parse.quote(PATH)
        encoded_remarks = urllib.parse.quote(remarks)
        
        # 按照 VLESS 格式拼接完整的链接字符串
        # 注意：host 参数用于 TLS SNI，这对于使用域名至关重要
        vless_link = (
            f"vless://{USER_ID}@{address}:{PORT}?"
            f"encryption=none&security=tls&sni={host}&type=ws&host={host}&path={encoded_path}"
            f"#{encoded_remarks}"
        )
        all_vless_links.append(vless_link)
        
    return all_vless_links

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 执行域名读取
    domains = read_domains()
    
    # 如果读取失败或没有域名，则终止程序
    if domains is None or not domains:
        print("\n❌ 因无法获取域名，程序终止。")
        sys.exit(1) # 退出并返回错误码，GitHub Actions 会将此次运行标记为失败
    
    # 2. 根据域名列表生成链接
    vless_links = generate_vless_links(domains)
    
    # 3. 将所有生成的链接写入文件（'w' 模式会覆盖旧文件）
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(vless_links))
        print(f"\n✅ 成功！所有 {len(vless_links)} 条链接已根据 '{DOMAINS_FILE}' 的内容覆盖写入到 '{OUTPUT_FILE}' 文件中。")
    except IOError as e:
        print(f"\n❌ 写入文件失败: {e}")
        sys.exit(1)
