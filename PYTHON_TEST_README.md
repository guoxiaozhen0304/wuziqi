# Python版本测试使用说明

## 安装依赖

### 1. 安装Python依赖包

```bash
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器

```bash
playwright install chromium
```

## 运行测试

### 方式一：直接运行Python脚本

```bash
python test_wuziqi.py
```

### 方式二：使用pytest运行（如果安装了pytest-playwright）

```bash
pytest test_wuziqi.py -v
```

## 测试说明

### 测试用例列表

Python脚本包含以下15个测试用例：

1. **TC001** - 页面加载测试
2. **TC002** - 棋盘样式测试
3. **TC003** - 首次落子测试
4. **TC004** - 轮流下棋测试
5. **TC005** - 重复位置测试
6. **TC006** - 重新开始功能测试
7. **TC007** - 棋盘边缘落子测试
8. **TC010** - 横向五子连珠测试
9. **TC011** - 纵向五子连珠测试
10. **TC012** - 左斜向五子连珠测试
11. **TC013** - 右斜向五子连珠测试
12. **TC017** - 四子不获胜测试
13. **TC018** - 获胜后点击测试
14. **TC019** - 获胜后重新开始测试
15. **TC020** - 快速连续点击测试

### 测试特点

- ✅ 使用Playwright Python异步API
- ✅ 自动处理alert对话框
- ✅ 详细的测试结果输出
- ✅ 支持有头模式（可以看到浏览器操作）
- ✅ 每个测试独立运行，互不影响

### 输出示例

```
============================================================
五子棋游戏自动化测试 - Python版本
============================================================

✅ TC001 - 页面加载测试 - 通过
✅ TC002 - 棋盘样式测试 - 通过
✅ TC003 - 首次落子测试 - 通过
...

============================================================
测试总结
============================================================
总计: 15 个测试
✅ 通过: 15
❌ 失败: 0
============================================================
```

## 自定义测试

### 修改为无头模式

在 `test_wuziqi.py` 中找到这一行：

```python
self.browser = await playwright.chromium.launch(headless=False)
```

改为：

```python
self.browser = await playwright.chromium.launch(headless=True)
```

### 运行单个测试

可以修改 `run_all_tests()` 方法中的 `tests` 列表，只保留想要运行的测试。

### 添加新测试

在 `WuziqiTest` 类中添加新的测试方法：

```python
async def test_tc_new(self):
    """新测试用例"""
    # 测试代码
    pass
```

然后在 `run_all_tests()` 的 `tests` 列表中添加：

```python
("TC_NEW - 新测试", self.test_tc_new),
```

## 注意事项

1. 确保 `index.html` 文件在同一目录下
2. Python版本建议 3.8 或更高
3. 测试会自动打开浏览器窗口（有头模式）
4. 每个测试之间会自动重新加载页面

## 故障排除

### 问题：找不到playwright模块

```bash
pip install playwright
playwright install chromium
```

### 问题：浏览器启动失败

确保已经安装了Chromium浏览器：

```bash
playwright install chromium
```

### 问题：测试超时

可以在测试代码中增加等待时间：

```python
await self.page.wait_for_timeout(1000)  # 等待1秒
```
