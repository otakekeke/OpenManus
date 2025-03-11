import asyncio

from app.agent.manus import Manus
from app.logger import logger


async def main():
    agent = Manus()
    while True:
        try:
            prompt = input("プロンプトを入力してください（終了するには 'exit'/'quit'）: ")
            prompt_lower = prompt.lower()
            if prompt_lower in ["exit", "quit"]:
                logger.info("さようなら！")
                break
            if not prompt.strip():
                logger.warning("空のプロンプトはスキップします。")
                continue
            logger.warning("リクエストを処理中...")
            await agent.run(prompt)
        except KeyboardInterrupt:
            logger.warning("さようなら！")
            break


if __name__ == "__main__":
    asyncio.run(main())
