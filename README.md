# 本项目为StreamFlow协同知识建构平台项目服务端代码

# git提交规范
1. init - 项目初始化
2. feat - 新功能 feature
3. fix - 修复 bug
4. docs - 文档注释
5. style - 代码格式(不影响代码运行的变动)
6. refactor - 重构、优化(既不增加新功能，也不是修复bug)
7. perf - 性能优化
8. test - 增加测试
9. chore - 构建过程或辅助工具的变动
10. revert - 回退
11. build - 打包

# 项目结构
-- apis  存放所有路由的接口
    api_router.py  各模块路由文件
    -- controller  存放所有路由的接口控制器
-- core 配置项存放
-- crud  各模块数据库操作模块
--db 数据库连接
--models 数据库模型
--register 中间件
--schemas 数据校验
--utils 工具