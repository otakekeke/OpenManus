import asyncio
import time

from app.agent.manus import Manus
from app.flow.base import FlowType
from app.flow.flow_factory import FlowFactory
from app.logger import logger


async def run_flow():
    agents = {
        "manus": Manus(),
    }

    while True:
        try:
            prompt = input("プロンプトを入力してください（終了するには 'exit'）: ")
            if prompt.lower() == "exit":
                logger.info("さようなら！")
                break

            flow = FlowFactory.create_flow(
                flow_type=FlowType.PLANNING,
                agents=agents,
            )
            if prompt.strip().isspace():
                logger.warning("空のプロンプトはスキップします。")
                continue
            logger.warning("リクエストを処理中...")

            try:
                start_time = time.time()
                result = await asyncio.wait_for(
                    flow.execute(prompt),
                    timeout=3600,  # 60分のタイムアウト（実行全体）
                )
                elapsed_time = time.time() - start_time
                logger.info(f"リクエストは {elapsed_time:.2f} 秒で処理されました")
                logger.info(result)
            except asyncio.TimeoutError:
                logger.error("リクエスト処理が1時間後にタイムアウトしました")
                logger.info(
                    "タイムアウトにより操作が終了しました。より簡単なリクエストを試してください。"
                )

        except KeyboardInterrupt:
            logger.info("ユーザーによって操作がキャンセルされました。")
        except Exception as e:
            logger.error(f"エラー: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_flow())
