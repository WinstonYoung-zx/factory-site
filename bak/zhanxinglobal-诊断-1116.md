# ZHANXIN GLOBAL 第 23 轮线上诊断（2026-11-16 13:10）

## 结论速览

站点技术面健康，无新增缺陷。上一轮（第 22 轮）三项整改 + 本轮 WebP 优化均已正确部署到源站。
**唯一需要处理的运营动作：Cloudflare 边缘缓存未刷新，导致 WebP 优化对真实访客"尚未生效"。** 这不是代码问题，是一次缓存清除操作即可解决。

| 项目 | 状态 |
|---|---|
| 站点可达 / 全站 URL | 137/137 返回 200 |
| 产品页静态化（第22轮） | 生效：8 条 Feature 直出、词典 defer、空 i18n=0 |
| WebP 优化（本轮提交） | **源站已生效，CDN 缓存未刷新** ⚠️ |
| title / description 规范 | >65 = 0，>170 = 0，缺失 = 0 |
| canonical 自指 / JSON-LD | 全自指，解析失败 0 |
| 安全头 / 缓存头 | 齐全（HSTS/CSP/CORP 等） |

---

## 一、⚠️ 唯一行动项：WebP 已被 CDN 旧缓存"挡住"

**现象（实测证据）：**

- 本地 `HEAD = origin/main = 937e657`，代码已全部 push；`uploads/` 下 149 张 webp 已生成。
- WebP 资源文件线上已上传成功：`/uploads/banner1.webp`、`/uploads/busshelter.webp`、`/uploads/blog/*.webp`、`/uploads/r400/*.webp` 全部 **200**；原 jpg 也仍在（200），无 404 风险。
- 源站 HTML 已是新版：本地首页 33 处 `.webp` / 9 处 `.jpg`；绕过 CDN 加随机参数（MISS）实测线上首页同样 **33 webp / 9 jpg**。
- **但普通访客拿到的仍是旧页**：直接请求首页返回 **0 webp / 42 jpg**，`style.css` 线上 0 webp（本地 2 webp）。

**根因：** 首页 HTTP 头 `cf-cache-status: HIT`，`Age: 80059`（约 22.2 小时），而声明的 `cache-control: max-age=600`。边缘节点缓存的是 11-15 的旧版本，尚未回源取新页。`must-revalidate` 未在 CDN 层触发预期回源。

**影响：** WebP 的体积收益（本轮 266 文件改动）当前对真实用户为 0；页面仍加载全量 JPEG。对收录无影响，但性能优化未兑现。

**处理（二选一，30 秒完成）：**
1. 推荐：Cloudflare Dashboard → Caching → Configuration → **Purge Everything**（清理全站缓存）；
2. 或精准清除：对 `https://www.zhanxinglobal.com/` 与 `https://www.zhanxinglobal.com/style.css` 做 **Purge by URL**（缓存按 URL 缓存，含 query 变体需填对应 URL）。

**验证方法：** 清除后用不带任何 query 参数的 `curl https://www.zhanxinglobal.com/ | grep -o '\.webp' | wc -l`，应返回约 33（非 0）。

> 附带提醒：`_headers` 中 `/*.html` 类是 `max-age=600, must-revalidate`（10 分钟），但缓存 Age 达 22 小时，说明 Cloudflare 侧可能有 Page Rule / Cache Rule 覆盖了源站缓存头。若清除后仍有异常，可检查 CF 缓存规则配置。

---

## 二、健康项（不用管）

- **可达性**：137/137 URL 全 200，平均首字节约 1.2s，Cloudflare Brotli + CDN。
- **元数据**：title>65 = 0、desc>170 = 0、desc 缺失 = 0；最长 title 65 字符（合规上限内）。
- **规范化**：canonical 全部自指；JSON-LD 结构化数据 0 解析失败；og:image / twitter:image 全部保留 `.jpg`（符合"社交爬虫兼容"既定策略，未被误改成 webp）。
- **图片**：全站 webp 引用 1128 / jpg 580 —— WebP 改写覆盖到位且未一刀切。
- **产品页**（承接第 22 轮复查）：Feature 8 条英文直出、词典 `product-*.js` 带 `defer`、空 data-i18n = 0、主图 preload 均在。
- ** robots.txt**：屏蔽 GPTBot/CCBot（训练类），放行 ClaudeBot/PerplexityBot/OAI-SearchBot（搜索引用类），与"产品页静态直出让 AI 可引用"策略自洽。

## 三、两个"看似异常"实为正常（已排除）

1. **18 页 hreflang = 0**：这些是 4 个静态页（privacy/certificates/faq/cases）+ 14 个产品页。它们本就没有多语言副本，与前几轮"118 页×8 闭环"记录一致，属既定架构，非回归缺陷。若要补齐需先生成这些页的 7 语言副本，成本高、收益低，暂不建议。
2. **7 页 products 各 1 张图"缺宽高"**：实为正则误报——命中的是 JS 模板字符串 `<img src="' + escapeHtml(imgSrc) + '...">`，并非真实渲染 DOM 图片，无需处理。

---

## 四、下一步建议（优先级）

1. **立即**：Cloudflare Purge Everything，并按上文方法验证 webp 生效（这是本轮唯一待办）。
2. **可选**：GSC 重新提交 sitemap（137 条），请求对近期更新的产品页/博客重新编目。
3. **下一阶段方向**：站内技术面已无明显短板，重心应转向外链建设与内容分发（第 22 轮已提出，本轮维持）。

诊断脚本：`bak/audit23.py`（绕过 CDN 缓存直取源站，可复跑）；数据：`bak/_audit23.json`。
