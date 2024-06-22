import requests
import sys
import logging
import json

DEFAULT_HEADERS = {"Content-Type": "application/json"}
RPC = 'https://api.mainnet-beta.solana.com'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

def do_request(url_: str, method_: str = 'GET', data_: str = '', timeout_: int = 3,
               headers_: dict = None):
    if headers_ is None:
        headers_ = DEFAULT_HEADERS
    try:
        if method_.lower() == 'get':
            r = requests.get(url_, headers=headers_, timeout=(timeout_, timeout_))
        elif method_.lower() == 'post':
            r = requests.post(url_, headers=headers_, data=data_, timeout=(timeout_, timeout_))
        elif method_.lower() == 'head':
            r = requests.head(url_, headers=headers_, timeout=(timeout_, timeout_))
        return r
    except Exception as reqErr:
        return f'error in do_request(): {reqErr}'

def get_all_rpc_ips():
    logger.info("get_all_rpc_ips()")
    d = '{"jsonrpc":"2.0", "id":1, "method":"getClusterNodes"}'
    r = do_request(url_=RPC, method_='post', data_=d, timeout_=25)
    if 'result' in str(r.text):
        rpc_ips = [node["rpc"] for node in r.json()["result"] if node["rpc"] is not None]
        rpc_ips = list(set(rpc_ips))  # remove duplicates
        return rpc_ips
    else:
        logger.error(f'Can\'t get RPC ip addresses {r.text}')
        sys.exit()

def main():
    rpc_nodes = get_all_rpc_ips()
    logger.info(f'RPC servers found: {len(rpc_nodes)}')
    for rpc in rpc_nodes:
        print(rpc)

if __name__ == "__main__":
    main()
