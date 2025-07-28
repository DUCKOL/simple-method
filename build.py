import urllib.parse
import sys

# --- VLESS 配置参数 (请勿修改) ---
USER_ID = '2e24b381-09e5-4386-b8c2-033c1bc40b12'
PORT = 443
PATH = '/?ed=2560'
REMARKS_PREFIX = '@ys==>unlock all'

# --- 新的文件名定义 ---
SOURCE_FILE = 'config.txt'        # <-- 读取这个新文件
OUTPUT_FILE = 'vless_links.txt'   # <-- 输出到这个文件

def get_domain_from_config():
    """从 config.txt 文件读取第一个有效的域名。"""
    print(f"[*] 正在从 '{SOURCE_FILE}' 文件读取配置...")
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                # 忽略空行和以'#'开头的注释行
                if domain and not domain.startswith('#'):
                    print(f"[+] 成功找到域名: {domain}")
                    return domain
        
        print(f"[-] 警告: 在 '{SOURCE_FILE}' 中未找到任何可用的域名。")
        return None
        
    except FileNotFoundError:
        print(f"[!] 致命错误: 源文件 '{SOURCE_FILE}' 不存在！")
        return None
    except Exception as e:
        print(f"[!] 读取文件时发生错误: {e}")
        return None

def create_vless_link(domain):
    """为指定的域名创建 VLESS 链接。"""
    print(f"[*] 正在为域名 '{domain}' 构建链接...")
    address = domain
    host = domain
    remarks = f"{REMARKS_PREFIX} {domain}"
    
    encoded_path = urllib.parse.quote(PATH)
    encoded_remarks = urllib.parse.quote(remarks)
    
    # 拼接最终的 VLESS 链接
    vless_link = (
        f"vless://{USER_ID}@{address}:{PORT}?"
        f"encryption=none&security=tls&sni={host}&type=ws&host={host}&path={encoded_path}"
        f"#{encoded_remarks}"
    )
    return vless_link

# --- 主程序 ---
if __name__ == "__main__":
    print("--- 开始执行自动生成任务 ---")
    
    # 1. 获取域名
    target_domain = get_domain_from_config()
    
    # 2. 如果没有域名，则失败并退出
    if not target_domain:
        print("\n[!] 程序因缺少域名而终止。")
        sys.exit(1)
    
    # 3. 生成链接
    final_link = create_vless_link(target_domain)
    
    # 4. 写入文件，覆盖旧内容
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(final_link + '\n') # 在链接末尾加一个换行符
        print(f"[+] 任务成功！链接已写入 '{OUTPUT_FILE}'。")
    except IOError as e:
        print(f"[!] 写入输出文件时出错: {e}")
        sys.exit(1)
        
    print("--- 任务执行完毕 ---")
