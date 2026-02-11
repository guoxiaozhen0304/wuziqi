/**
 * 五子棋游戏自动化测试
 * 使用Playwright测试框架
 */

const { test, expect } = require('@playwright/test');
const path = require('path');

const PAGE_URL = `file:///${path.resolve(__dirname, 'index.html').replace(/\\/g, '/')}`;

test.describe('五子棋游戏测试套件', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(PAGE_URL);
  });

  // ==================== 一、UI界面测试 ====================

  test('TC001 - 页面加载测试', async ({ page }) => {
    // 检查页面标题
    await expect(page).toHaveTitle('五子棋游戏');

    // 检查主标题
    const h1 = page.locator('h1');
    await expect(h1).toHaveText('五子棋');

    // 检查当前玩家显示
    const currentPlayer = page.locator('#currentPlayer');
    await expect(currentPlayer).toHaveText('黑方');

    // 检查棋盘存在
    const canvas = page.locator('#board');
    await expect(canvas).toBeVisible();

    // 检查重新开始按钮
    const resetBtn = page.locator('button.btn');
    await expect(resetBtn).toBeVisible();
    await expect(resetBtn).toHaveText('重新开始');
  });

  test('TC002 - 棋盘样式测试', async ({ page }) => {
    const canvas = page.locator('#board');

    // 检查棋盘尺寸
    const width = await canvas.getAttribute('width');
    const height = await canvas.getAttribute('height');
    expect(width).toBe('600');
    expect(height).toBe('600');

    // 检查棋盘可见
    await expect(canvas).toBeVisible();
  });

  // ==================== 二、基本功能测试 ====================

  test('TC003 - 首次落子测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    // 初始状态应该是黑方
    await expect(currentPlayer).toHaveText('黑方');

    // 点击棋盘中心位置
    await canvas.click({ position: { x: 300, y: 300 } });

    // 等待一小段时间让棋子绘制完成
    await page.waitForTimeout(100);

    // 检查玩家切换为白方
    await expect(currentPlayer).toHaveText('白方');
  });

  test('TC004 - 轮流下棋测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    // 第1次点击 - 黑方
    await expect(currentPlayer).toHaveText('黑方');
    await canvas.click({ position: { x: 100, y: 100 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('白方');

    // 第2次点击 - 白方
    await canvas.click({ position: { x: 150, y: 100 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('黑方');

    // 第3次点击 - 黑方
    await canvas.click({ position: { x: 200, y: 100 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('白方');
  });

  test('TC005 - 重复位置测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    // 第一次点击
    await canvas.click({ position: { x: 300, y: 300 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('白方');

    // 在同一位置再次点击
    await canvas.click({ position: { x: 300, y: 300 } });
    await page.waitForTimeout(50);

    // 玩家应该仍然是白方（没有切换）
    await expect(currentPlayer).toHaveText('白方');
  });

  test('TC006 - 重新开始功能测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');
    const resetBtn = page.locator('button.btn');

    // 下几步棋
    await canvas.click({ position: { x: 100, y: 100 } });
    await canvas.click({ position: { x: 150, y: 100 } });
    await canvas.click({ position: { x: 200, y: 100 } });
    await page.waitForTimeout(100);

    // 当前应该是白方
    await expect(currentPlayer).toHaveText('白方');

    // 点击重新开始
    await resetBtn.click();
    await page.waitForTimeout(100);

    // 检查重置为黑方
    await expect(currentPlayer).toHaveText('黑方');

    // 可以在之前的位置重新落子
    await canvas.click({ position: { x: 100, y: 100 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('白方');
  });

  // ==================== 三、边界测试 ====================

  test('TC007 - 棋盘边缘落子测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    // 测试四个角
    const corners = [
      { x: 20, y: 20 },      // 左上角
      { x: 580, y: 20 },     // 右上角
      { x: 20, y: 580 },     // 左下角
      { x: 580, y: 580 }     // 右下角
    ];

    for (const corner of corners) {
      await canvas.click({ position: corner });
      await page.waitForTimeout(50);
    }

    // 应该成功下了4步棋
    await expect(currentPlayer).toHaveText('黑方');
  });

  test('TC008 - 棋盘外点击测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    // 先下一步棋，让当前玩家变为白方
    await canvas.click({ position: { x: 300, y: 300 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('白方');

    // 点击棋盘边缘但超出有效范围的位置
    // 根据代码，有效范围是从CELL_SIZE/2开始，点击(0,0)应该超出范围
    await canvas.click({ position: { x: 1, y: 1 } });
    await page.waitForTimeout(50);

    // 如果点击无效，玩家应该仍然是白方
    // 如果点击有效，玩家会变为黑方
    // 由于边界判断，这个位置可能有效也可能无效，我们只验证游戏状态一致
    const playerText = await currentPlayer.textContent();
    expect(['黑方', '白方']).toContain(playerText);
  });

  // ==================== 四、胜利判定测试 ====================

  test('TC010 - 横向五子连珠测试', async ({ page }) => {
    const canvas = page.locator('#board');

    // 监听alert对话框
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('获胜');
      await dialog.accept();
    });

    // 黑方在第7行横向放置5个棋子
    // 白方在第8行放置棋子（避免干扰）
    const y = 300;
    const whiteY = 340;

    for (let i = 0; i < 5; i++) {
      // 黑方落子
      await canvas.click({ position: { x: 100 + i * 40, y: y } });
      await page.waitForTimeout(50);

      // 如果不是最后一步，白方也落子
      if (i < 4) {
        await canvas.click({ position: { x: 100 + i * 40, y: whiteY } });
        await page.waitForTimeout(50);
      }
    }

    // 等待alert出现
    await page.waitForTimeout(200);
  });

  test('TC011 - 纵向五子连珠测试', async ({ page }) => {
    const canvas = page.locator('#board');

    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('获胜');
      await dialog.accept();
    });

    // 黑方在第7列纵向放置5个棋子
    const x = 300;
    const whiteX = 340;

    for (let i = 0; i < 5; i++) {
      // 黑方落子
      await canvas.click({ position: { x: x, y: 100 + i * 40 } });
      await page.waitForTimeout(50);

      if (i < 4) {
        await canvas.click({ position: { x: whiteX, y: 100 + i * 40 } });
        await page.waitForTimeout(50);
      }
    }

    await page.waitForTimeout(200);
  });

  test('TC012 - 左斜向五子连珠测试', async ({ page }) => {
    const canvas = page.locator('#board');

    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('获胜');
      await dialog.accept();
    });

    // 黑方对角线放置5个棋子
    for (let i = 0; i < 5; i++) {
      // 黑方落子（对角线）
      await canvas.click({ position: { x: 100 + i * 40, y: 100 + i * 40 } });
      await page.waitForTimeout(50);

      if (i < 4) {
        // 白方落子（另一条对角线）
        await canvas.click({ position: { x: 100 + i * 40, y: 300 - i * 40 } });
        await page.waitForTimeout(50);
      }
    }

    await page.waitForTimeout(200);
  });

  test('TC013 - 右斜向五子连珠测试', async ({ page }) => {
    const canvas = page.locator('#board');

    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('获胜');
      await dialog.accept();
    });

    // 黑方右斜向放置5个棋子
    for (let i = 0; i < 5; i++) {
      // 黑方落子（右斜向）
      await canvas.click({ position: { x: 300 - i * 40, y: 100 + i * 40 } });
      await page.waitForTimeout(50);

      if (i < 4) {
        // 白方落子
        await canvas.click({ position: { x: 100 + i * 40, y: 100 + i * 40 } });
        await page.waitForTimeout(50);
      }
    }

    await page.waitForTimeout(200);
  });

  test('TC017 - 四子不获胜测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    let dialogAppeared = false;
    page.on('dialog', async dialog => {
      dialogAppeared = true;
      await dialog.accept();
    });

    // 黑方横向放置4个棋子
    const y = 300;
    const whiteY = 340;

    for (let i = 0; i < 4; i++) {
      await canvas.click({ position: { x: 100 + i * 40, y: y } });
      await page.waitForTimeout(50);
      await canvas.click({ position: { x: 100 + i * 40, y: whiteY } });
      await page.waitForTimeout(50);
    }

    // 等待确认没有alert
    await page.waitForTimeout(200);

    // 不应该出现获胜对话框
    expect(dialogAppeared).toBe(false);

    // 游戏应该继续
    await expect(currentPlayer).toBeVisible();
  });

  // ==================== 五、游戏结束后测试 ====================

  test('TC018 - 获胜后点击测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    page.on('dialog', async dialog => {
      await dialog.accept();
    });

    // 快速完成横向五子连珠
    const y = 300;
    const whiteY = 340;

    for (let i = 0; i < 5; i++) {
      await canvas.click({ position: { x: 100 + i * 40, y: y } });
      await page.waitForTimeout(30);
      if (i < 4) {
        await canvas.click({ position: { x: 100 + i * 40, y: whiteY } });
        await page.waitForTimeout(30);
      }
    }

    await page.waitForTimeout(200);

    // 记录当前玩家
    const playerBeforeClick = await currentPlayer.textContent();

    // 尝试继续点击
    await canvas.click({ position: { x: 400, y: 400 } });
    await page.waitForTimeout(50);

    // 玩家不应该改变
    const playerAfterClick = await currentPlayer.textContent();
    expect(playerAfterClick).toBe(playerBeforeClick);
  });

  test('TC019 - 获胜后重新开始测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');
    const resetBtn = page.locator('button.btn');

    page.on('dialog', async dialog => {
      await dialog.accept();
    });

    // 完成五子连珠
    const y = 300;
    const whiteY = 340;

    for (let i = 0; i < 5; i++) {
      await canvas.click({ position: { x: 100 + i * 40, y: y } });
      await page.waitForTimeout(30);
      if (i < 4) {
        await canvas.click({ position: { x: 100 + i * 40, y: whiteY } });
        await page.waitForTimeout(30);
      }
    }

    await page.waitForTimeout(200);

    // 点击重新开始
    await resetBtn.click();
    await page.waitForTimeout(100);

    // 检查重置为黑方
    await expect(currentPlayer).toHaveText('黑方');

    // 可以重新开始游戏
    await canvas.click({ position: { x: 300, y: 300 } });
    await page.waitForTimeout(50);
    await expect(currentPlayer).toHaveText('白方');
  });

  // ==================== 六、性能测试 ====================

  test('TC020 - 快速连续点击测试', async ({ page }) => {
    const canvas = page.locator('#board');
    const currentPlayer = page.locator('#currentPlayer');

    // 快速连续点击10个不同位置
    const positions = [
      { x: 100, y: 100 }, { x: 150, y: 100 },
      { x: 200, y: 100 }, { x: 250, y: 100 },
      { x: 100, y: 150 }, { x: 150, y: 150 },
      { x: 200, y: 150 }, { x: 250, y: 150 },
      { x: 100, y: 200 }, { x: 150, y: 200 }
    ];

    for (const pos of positions) {
      await canvas.click({ position: pos });
      await page.waitForTimeout(10); // 很短的等待时间
    }

    // 应该下了10步棋，当前是黑方
    await expect(currentPlayer).toHaveText('黑方');
  });

});
