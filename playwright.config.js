const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './',
  testMatch: '**/*.spec.js',

  // 测试超时时间
  timeout: 30000,

  // 期望超时时间
  expect: {
    timeout: 5000
  },

  // 失败时重试次数
  retries: 0,

  // 并行执行的worker数量
  workers: 1,

  // 报告配置
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list']
  ],

  use: {
    // 基础URL
    baseURL: 'file:///',

    // 截图配置
    screenshot: 'only-on-failure',

    // 视频配置
    video: 'retain-on-failure',

    // 追踪配置
    trace: 'on-first-retry',
  },

  // 测试项目配置
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
