# 五子棋游戏自动化测试

## 测试覆盖范围

本测试套件包含以下测试用例：

### 一、UI界面测试
- TC001: 页面加载测试
- TC002: 棋盘样式测试

### 二、基本功能测试
- TC003: 首次落子测试
- TC004: 轮流下棋测试
- TC005: 重复位置测试
- TC006: 重新开始功能测试

### 三、边界测试
- TC007: 棋盘边缘落子测试
- TC008: 棋盘外点击测试

### 四、胜利判定测试
- TC010: 横向五子连珠测试
- TC011: 纵向五子连珠测试
- TC012: 左斜向五子连珠测试
- TC013: 右斜向五子连珠测试
- TC017: 四子不获胜测试

### 五、游戏结束后测试
- TC018: 获胜后点击测试
- TC019: 获胜后重新开始测试

### 六、性能测试
- TC020: 快速连续点击测试

## 安装依赖

```bash
npm install
```

## 运行测试

### 运行所有测试（无头模式）
```bash
npm test
```

### 运行测试（有头模式，可以看到浏览器）
```bash
npm run test:headed
```

### 使用UI模式运行测试
```bash
npm run test:ui
```

### 调试模式运行测试
```bash
npm run test:debug
```

### 只在特定浏览器运行测试
```bash
npm run test:chromium   # Chrome浏览器
npm run test:firefox    # Firefox浏览器
npm run test:webkit     # Safari浏览器
```

### 查看测试报告
```bash
npm run report
```

## 测试结果

测试完成后会生成：
- HTML测试报告（playwright-report目录）
- 失败时的截图
- 失败时的视频录制
- 追踪文件（用于调试）

## 文件说明

- `wuziqi.spec.js` - 测试用例文件
- `playwright.config.js` - Playwright配置文件
- `package.json` - 项目依赖配置
- `index.html` - 被测试的五子棋游戏页面

## 注意事项

1. 首次运行需要安装Playwright浏览器：
   ```bash
   npx playwright install
   ```

2. 测试使用本地文件协议（file:///）访问HTML页面

3. 所有测试都会自动处理alert对话框

4. 测试包含适当的等待时间以确保动画和渲染完成
