import logging
import os
# 創建自定義日誌器
logger = logging.getLogger('wootalk_bot_log')

# 設置日誌等級
logger.setLevel(logging.DEBUG)


log_directory = r'.\log'


# 創建處理器 (Handler)，例如控制台處理器和文件處理器
console_handler = logging.StreamHandler()  # 控制台處理器
# 如果目錄不存在，則創建它
if not os.path.exists(r'.\log'):
    os.makedirs(r'.\log')
file_handler = logging.FileHandler(r'.\log\run.log', encoding='utf-8')  # 文件處理器

# 設置處理器的日誌等級
console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.DEBUG)

# 創建並設置日誌格式器 (Formatter)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 將處理器添加到日誌器

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 記錄日誌訊息
logger.debug("這是 DEBUG 級別的訊息")
logger.info("這是 INFO 級別的訊息")
logger.warning("這是 WARNING 級別的訊息")
logger.error("這是 ERROR 級別的訊息")
logger.critical("這是 CRITICAL 級別的訊息")
