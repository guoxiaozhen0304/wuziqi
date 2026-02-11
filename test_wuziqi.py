"""
五子棋游戏自动化测试 - Python版本
使用 Playwright Python 库执行测试
"""

import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, expect

# 设置UTF-8编码输出，解决Windows中文显示问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 获取HTML文件的绝对路径
CURRENT_DIR = Path(__file__).parent
PAGE_URL = f"file:///{CURRENT_DIR / 'index.html'}".replace("\\", "/")


class WuziqiTest:
    """五子棋测试类"""

    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.passed = 0
        self.failed = 0
        self.test_results = []

    async def setup(self, playwright):
        """初始化浏览器"""
        self.browser = await playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def teardown(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()

    async def goto_page(self):
        """导航到页面"""
        await self.page.goto(PAGE_URL)
        await self.page.wait_for_timeout(500)

    def log_test(self, test_name, status, error=None):
        """记录测试结果"""
        if status == "PASS":
            self.passed += 1
            print(f"✅ {test_name} - 通过")
        else:
            self.failed += 1
            print(f"❌ {test_name} - 失败")
            if error:
                print(f"   错误: {error}")

        self.test_results.append({
            "name": test_name,
            "status": status,
            "error": error
        })

    async def run_test(self, test_name, test_func):
        """运行单个测试"""
        try:
            await self.goto_page()
            await test_func()
            self.log_test(test_name, "PASS")
        except Exception as e:
            self.log_test(test_name, "FAIL", str(e))

    # ==================== 测试用例 ====================

    async def test_tc001_page_load(self):
        """TC001 - 页面加载测试"""
        # 检查页面标题
        assert await self.page.title() == "五子棋游戏"

        # 检查主标题
        h1 = self.page.locator("h1")
        await expect(h1).to_have_text("五子棋")

        # 检查当前玩家显示
        current_player = self.page.locator("#currentPlayer")
        await expect(current_player).to_have_text("黑方")

        # 检查棋盘存在
        canvas = self.page.locator("#board")
        await expect(canvas).to_be_visible()

        # 检查重新开始按钮
        reset_btn = self.page.locator("button.btn")
        await expect(reset_btn).to_be_visible()
        await expect(reset_btn).to_have_text("重新开始")

    async def test_tc002_board_style(self):
        """TC002 - 棋盘样式测试"""
        canvas = self.page.locator("#board")

        # 检查棋盘尺寸
        width = await canvas.get_attribute("width")
        height = await canvas.get_attribute("height")
        assert width == "600"
        assert height == "600"

        # 检查棋盘可见
        await expect(canvas).to_be_visible()

    async def test_tc003_first_move(self):
        """TC003 - 首次落子测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")

        # 初始状态应该是黑方
        await expect(current_player).to_have_text("黑方")

        # 点击棋盘中心位置
        await canvas.click(position={"x": 300, "y": 300})
        await self.page.wait_for_timeout(100)

        # 检查玩家切换为白方
        await expect(current_player).to_have_text("白方")

    async def test_tc004_turn_based(self):
        """TC004 - 轮流下棋测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")

        # 第1次点击 - 黑方
        await expect(current_player).to_have_text("黑方")
        await canvas.click(position={"x": 100, "y": 100})
        await self.page.wait_for_timeout(50)
        await expect(current_player).to_have_text("白方")

        # 第2次点击 - 白方
        await canvas.click(position={"x": 150, "y": 100})
        await self.page.wait_for_timeout(50)
        await expect(current_player).to_have_text("黑方")

        # 第3次点击 - 黑方
        await canvas.click(position={"x": 200, "y": 100})
        await self.page.wait_for_timeout(50)
        await expect(current_player).to_have_text("白方")

    async def test_tc005_duplicate_position(self):
        """TC005 - 重复位置测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")

        # 第一次点击
        await canvas.click(position={"x": 300, "y": 300})
        await self.page.wait_for_timeout(50)
        await expect(current_player).to_have_text("白方")

        # 在同一位置再次点击
        await canvas.click(position={"x": 300, "y": 300})
        await self.page.wait_for_timeout(50)

        # 玩家应该仍然是白方（没有切换）
        await expect(current_player).to_have_text("白方")

    async def test_tc006_reset_game(self):
        """TC006 - 重新开始功能测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")
        reset_btn = self.page.locator("button.btn")

        # 下几步棋
        await canvas.click(position={"x": 100, "y": 100})
        await canvas.click(position={"x": 150, "y": 100})
        await canvas.click(position={"x": 200, "y": 100})
        await self.page.wait_for_timeout(100)

        # 当前应该是白方
        await expect(current_player).to_have_text("白方")

        # 点击重新开始
        await reset_btn.click()
        await self.page.wait_for_timeout(100)

        # 检查重置为黑方
        await expect(current_player).to_have_text("黑方")

        # 可以在之前的位置重新落子
        await canvas.click(position={"x": 100, "y": 100})
        await self.page.wait_for_timeout(50)
        await expect(current_player).to_have_text("白方")

    async def test_tc007_edge_positions(self):
        """TC007 - 棋盘边缘落子测试"""
        canvas = self.page.locator("#board")

        # 测试四个角
        corners = [
            {"x": 20, "y": 20},      # 左上角
            {"x": 580, "y": 20},     # 右上角
            {"x": 20, "y": 580},     # 左下角
            {"x": 580, "y": 580}     # 右下角
        ]

        for corner in corners:
            await canvas.click(position=corner)
            await self.page.wait_for_timeout(50)

        # 应该成功下了4步棋
        current_player = self.page.locator("#currentPlayer")
        await expect(current_player).to_have_text("黑方")

    async def test_tc010_horizontal_win(self):
        """TC010 - 横向五子连珠测试"""
        canvas = self.page.locator("#board")

        # 监听alert对话框
        dialog_message = None

        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 黑方在第7行横向放置5个棋子
        y = 300
        white_y = 340

        for i in range(5):
            # 黑方落子
            await canvas.click(position={"x": 100 + i * 40, "y": y})
            await self.page.wait_for_timeout(50)

            # 如果不是最后一步，白方也落子
            if i < 4:
                await canvas.click(position={"x": 100 + i * 40, "y": white_y})
                await self.page.wait_for_timeout(50)

        # 等待alert出现
        await self.page.wait_for_timeout(200)

        # 验证获胜提示
        assert dialog_message and "获胜" in dialog_message

    async def test_tc011_vertical_win(self):
        """TC011 - 纵向五子连珠测试"""
        canvas = self.page.locator("#board")

        dialog_message = None

        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 黑方在第7列纵向放置5个棋子
        x = 300
        white_x = 340

        for i in range(5):
            # 黑方落子
            await canvas.click(position={"x": x, "y": 100 + i * 40})
            await self.page.wait_for_timeout(50)

            if i < 4:
                await canvas.click(position={"x": white_x, "y": 100 + i * 40})
                await self.page.wait_for_timeout(50)

        await self.page.wait_for_timeout(200)
        assert dialog_message and "获胜" in dialog_message

    async def test_tc012_diagonal_left_win(self):
        """TC012 - 左斜向五子连珠测试"""
        canvas = self.page.locator("#board")

        dialog_message = None

        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 黑方对角线放置5个棋子
        for i in range(5):
            # 黑方落子（对角线）
            await canvas.click(position={"x": 100 + i * 40, "y": 100 + i * 40})
            await self.page.wait_for_timeout(50)

            if i < 4:
                # 白方落子（另一条对角线）
                await canvas.click(position={"x": 100 + i * 40, "y": 300 - i * 40})
                await self.page.wait_for_timeout(50)

        await self.page.wait_for_timeout(200)
        assert dialog_message and "获胜" in dialog_message

    async def test_tc013_diagonal_right_win(self):
        """TC013 - 右斜向五子连珠测试"""
        canvas = self.page.locator("#board")

        dialog_message = None

        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 黑方右斜向放置5个棋子
        for i in range(5):
            # 黑方落子（右斜向）
            await canvas.click(position={"x": 300 - i * 40, "y": 100 + i * 40})
            await self.page.wait_for_timeout(50)

            if i < 4:
                # 白方落子
                await canvas.click(position={"x": 100 + i * 40, "y": 100 + i * 40})
                await self.page.wait_for_timeout(50)

        await self.page.wait_for_timeout(200)
        assert dialog_message and "获胜" in dialog_message

    async def test_tc017_four_pieces_no_win(self):
        """TC017 - 四子不获胜测试"""
        canvas = self.page.locator("#board")

        dialog_appeared = False

        async def handle_dialog(dialog):
            nonlocal dialog_appeared
            dialog_appeared = True
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 黑方横向放置4个棋子
        y = 300
        white_y = 340

        for i in range(4):
            await canvas.click(position={"x": 100 + i * 40, "y": y})
            await self.page.wait_for_timeout(50)
            await canvas.click(position={"x": 100 + i * 40, "y": white_y})
            await self.page.wait_for_timeout(50)

        # 等待确认没有alert
        await self.page.wait_for_timeout(200)

        # 不应该出现获胜对话框
        assert not dialog_appeared

    async def test_tc018_click_after_win(self):
        """TC018 - 获胜后点击测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")

        async def handle_dialog(dialog):
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 快速完成横向五子连珠
        y = 300
        white_y = 340

        for i in range(5):
            await canvas.click(position={"x": 100 + i * 40, "y": y})
            await self.page.wait_for_timeout(30)
            if i < 4:
                await canvas.click(position={"x": 100 + i * 40, "y": white_y})
                await self.page.wait_for_timeout(30)

        await self.page.wait_for_timeout(200)

        # 记录当前玩家
        player_before = await current_player.text_content()

        # 尝试继续点击
        await canvas.click(position={"x": 400, "y": 400})
        await self.page.wait_for_timeout(50)

        # 玩家不应该改变
        player_after = await current_player.text_content()
        assert player_after == player_before

    async def test_tc019_reset_after_win(self):
        """TC019 - 获胜后重新开始测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")
        reset_btn = self.page.locator("button.btn")

        async def handle_dialog(dialog):
            await dialog.accept()

        self.page.on("dialog", handle_dialog)

        # 完成五子连珠
        y = 300
        white_y = 340

        for i in range(5):
            await canvas.click(position={"x": 100 + i * 40, "y": y})
            await self.page.wait_for_timeout(30)
            if i < 4:
                await canvas.click(position={"x": 100 + i * 40, "y": white_y})
                await self.page.wait_for_timeout(30)

        await self.page.wait_for_timeout(200)

        # 点击重新开始
        await reset_btn.click()
        await self.page.wait_for_timeout(100)

        # 检查重置为黑方
        await expect(current_player).to_have_text("黑方")

        # 可以重新开始游戏
        await canvas.click(position={"x": 300, "y": 300})
        await self.page.wait_for_timeout(50)
        await expect(current_player).to_have_text("白方")

    async def test_tc020_rapid_clicks(self):
        """TC020 - 快速连续点击测试"""
        canvas = self.page.locator("#board")
        current_player = self.page.locator("#currentPlayer")

        # 快速连续点击10个不同位置
        positions = [
            {"x": 100, "y": 100}, {"x": 150, "y": 100},
            {"x": 200, "y": 100}, {"x": 250, "y": 100},
            {"x": 100, "y": 150}, {"x": 150, "y": 150},
            {"x": 200, "y": 150}, {"x": 250, "y": 150},
            {"x": 100, "y": 200}, {"x": 150, "y": 200}
        ]

        for pos in positions:
            await canvas.click(position=pos)
            await self.page.wait_for_timeout(10)

        # 应该下了10步棋，当前是黑方
        await expect(current_player).to_have_text("黑方")

    async def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("五子棋游戏自动化测试 - Python版本")
        print("="*60 + "\n")

        tests = [
            ("TC001 - 页面加载测试", self.test_tc001_page_load),
            ("TC002 - 棋盘样式测试", self.test_tc002_board_style),
            ("TC003 - 首次落子测试", self.test_tc003_first_move),
            ("TC004 - 轮流下棋测试", self.test_tc004_turn_based),
            ("TC005 - 重复位置测试", self.test_tc005_duplicate_position),
            ("TC006 - 重新开始功能测试", self.test_tc006_reset_game),
            ("TC007 - 棋盘边缘落子测试", self.test_tc007_edge_positions),
            ("TC010 - 横向五子连珠测试", self.test_tc010_horizontal_win),
            ("TC011 - 纵向五子连珠测试", self.test_tc011_vertical_win),
            ("TC012 - 左斜向五子连珠测试", self.test_tc012_diagonal_left_win),
            ("TC013 - 右斜向五子连珠测试", self.test_tc013_diagonal_right_win),
            ("TC017 - 四子不获胜测试", self.test_tc017_four_pieces_no_win),
            ("TC018 - 获胜后点击测试", self.test_tc018_click_after_win),
            ("TC019 - 获胜后重新开始测试", self.test_tc019_reset_after_win),
            ("TC020 - 快速连续点击测试", self.test_tc020_rapid_clicks),
        ]

        async with async_playwright() as playwright:
            await self.setup(playwright)

            for test_name, test_func in tests:
                await self.run_test(test_name, test_func)

            await self.teardown()

        # 打印测试总结
        print("\n" + "="*60)
        print("测试总结")
        print("="*60)
        print(f"总计: {self.passed + self.failed} 个测试")
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print("="*60 + "\n")

        return self.failed == 0


async def main():
    """主函数"""
    test = WuziqiTest()
    success = await test.run_all_tests()

    # 返回退出码
    exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
