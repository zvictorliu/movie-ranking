# Three.js 圆柱画廊（Cylinder Gallery）实现原理

> 首页路由：`/`（全屏圆柱画廊）  
> 参考站：[k95.it](https://k95.it/en) 首页 `ThreeCylinderScene`  
> 本地实现：`web/src/components/three/ThreeCylinderScene.vue` + `web/src/views/HomePage.vue`

本文说明本仓库「电影封面圆柱画廊」的实现原理：布局数学、着色器、动画循环、交互与工程接入方式。

---

## 1. 要做什么

在相机位于圆柱**内侧**的视角下，把一批封面（`PlaneGeometry`）排布成可旋转的 3D 画廊，并支持两种布局：

| 模式 | 视觉效果 |
|------|----------|
| **Rings** | 若干水平圆环，封面按圈层叠 |
| **Spiral** | 同一批封面插值成螺旋，高低随角度变化 |

交互上：滚轮/拖拽旋转圆柱，悬停放大并显示片名，顶部切换 Rings ↔ Spiral。

---

## 2. 整体架构

```
HomePage.vue                  ThreeCylinderScene.vue
┌─────────────────────┐       ┌──────────────────────────────────┐
│ GET /api/movies     │ props │ Scene + PerspectiveCamera        │
│ 随机抽 10 条有封面  │─────▶│ WebGLRenderer → canvas            │
│ Rings/Spiral · 登录 │       │ rootGroup                        │
└─────────────────────┘       │   ├─ rowGroups[5] × panels[12]    │
                              │   └─ BackSide 网格背景圆柱       │
                              │ Raycaster / wheel / RAF 循环     │
                              └──────────────────────────────────┘
```

- **页面层**：调用后端影片列表，过滤有 `cover` 的条目后随机取最多 10 条；UI 含品牌、布局切换与登录入口。首页路由 `meta.hideChrome` 隐藏站点 Header/Footer。
- **场景层**：纯 Three.js 逻辑。用 `projects` + `spiral` 两个 props 驱动；封面 URL 使用 API 原样路径（经 `/imgs` 代理到后端）。网格为 Canvas 纹理贴在独立内侧圆柱上，不是封面圆柱的 LineSegments。

封面资源：由后端 `/api/movies` 返回的 `cover` 字段提供（通常为 `/imgs/covers/movie-cover/...`，经 Vite 代理到后端）。首页每次加载会**随机抽取最多 10 条**有封面的影片组成画廊；不足 10 条则用全部可用项。

技术栈：Vue 3 + Three.js **r183**（与参考站版本一致）。

---

## 3. 场景搭建

### 3.1 基础对象

```text
Scene.background = #0a0a1f
PerspectiveCamera(fov, aspect, 0.1, 200)   // fov / cameraZ 随断点变化
WebGLRenderer({ antialias, canvas })
  outputColorSpace = SRGB
  toneMapping = NoToneMapping              // 自定义着色器自行做 gamma
AmbientLight + DirectionalLight
rootGroup = Group()                        // 画廊与网格的父节点
```

相机放在原点附近、`z = cameraZ`，朝向场景中心，因此看到的是圆柱**内壁**上的面板。

### 3.2 响应式布局参数

按视口宽度/是否竖屏选择一组参数。面板按**影片封面横版 16:9**（`PANEL_ASPECT = 16/9`）计算：`panelW = baseH × 16/9 × PANEL_SCALE`。

| 断点 | fov | cameraZ | radius | panelW×H（约） | rowSpacing |
|------|-----|---------|--------|----------------|------------|
| 桌面默认 | 50 | 13 | 7.8 | 2.35×1.32 | 4.8 |
| 平板 / 窄屏 | 60–70 | 7.5–11 | 4.5–6.5 | 更小 | 3.2–4.2 |

`radius` 决定圆柱半径；`rowSpacing` 决定相邻圈的垂直间距（横版面板更矮，间距相应收紧）。

---

## 4. 布局数学（核心）

常量：

- `ROWS = 5`（圈数）
- `COLS = 12`（每圈面板数）
- 每圈用不同种子对项目列表洗牌，避免各圈封面顺序完全相同；不足 12 张时取模循环。

每个面板预先计算**两套**极坐标，供 Rings/Spiral 插值：

```text
thetaRing   = (col + row * 0.5) / COLS * 2π   // 相邻圈错开半格，更密实
thetaSpiral = col / COLS * 2π                 // 螺旋角与列对齐
ySpiral     = (col / COLS - 0.5) * rowSpacing // 螺旋时的垂直偏移
```

行组（`Group`）的基准高度：

```text
group.y = row * rowSpacing - (ROWS - 1) * rowSpacing / 2
```

### 4.1 混合函数 `applyLayoutBlend(t)`

`t ∈ [0, 1]`，`0 = Rings`，`1 = Spiral`：

```text
radius(t) = radiusBase * (1 + (0.72 - 1) * t)   // 螺旋时略收半径
θ(t)      = lerp(thetaRing, thetaSpiral, t)
x         = cos(θ) * radius(t)
z         = sin(θ) * radius(t)
y         = ySpiral * t                         // Rings 时 y=0，相对行组
rotation.y = -(θ - π/2)                         // 面板朝向圆心
```

UI 切换时并不瞬切：每帧用指数平滑逼近目标 `t`：

```text
spiralBlend += (spiralTarget - spiralBlend) * (1 - exp(-3.2 * dt))
```

这就是 Rings ↔ Spiral「软过渡」的来源。

---

## 5. 面板着色器

每个面板是独立的 `ShaderMaterial`（共享 `PlaneGeometry`，细分 `12×8` 以便顶点弯曲可见），`toneMapped: false`。

### 5.1 顶点着色器：弯曲 + 待机波

在 UV 中心化坐标上做抛物线拱：

```glsl
float xn = (uv.x - 0.5) * 2.0;  // -1 … +1
float yn = (uv.y - 0.5) * 2.0;
float archX = 1.0 - xn * xn;    // 中心 1，边缘 0
float archY = 1.0 - yn * yn;

pos.z -= archX * uBendH;        // 水平拱：跟自旋速度相关
pos.z -= archY * uBendV;        // 垂直拱：跟滚轮/滑动相关

// 待机微波：每片随机 uPhase，避免同步抖动
pos.z += sin(uv.y * 6.283 + uTime * 0.55 + uPhase)
       * sin(uv.x * 3.14  + uTime * 0.35 + uPhase * 1.3) * 0.016;
```

要点：**弯曲量由速度驱动，而不是由绝对转角驱动**。快速滚动时板子更「软」，停下后恢复平整。

### 5.2 片元着色器：景深染色 + 可选模糊

```text
采样纹理（可选 9-tap box blur，用于入场软焦）
depthT = smoothstep(uDepthNear, uDepthFar, vViewZ)
→ 远处略去饱和 + 混入深蓝灰色（uDepthColor）
→ linearToSRGB（pow 1/2.2）后输出
```

近处面板更鲜艳，远处偏冷灰，增强纵深而不必开后处理 Pass。

### 5.3 纹理

`TextureLoader` 加载封面（本仓库样例为 SVG，浏览器可解码为位图纹理）：

```text
colorSpace = SRGBColorSpace
minFilter  = LinearMipmapLinearFilter
```

同 URL 做缓存，避免 60 片重复请求。

---

## 6. 动画循环（手感来源）

每帧大致顺序：

```text
1. 平滑 spiralBlend，必要时 applyLayoutBlend
2. spinSmooth 跟随 spinTarget（滚轮累积）
3. spinDelta = spinSmooth - spinPrev          // 本帧角增量
4. bendRaw 指数衰减（pow(0.92, dt*60)）
5. spinAngle += (0.08 + bendRaw) * dt        // 怠速自转 + 输入
6. bendV / bendH 平滑到目标（来自 bendRaw / spinDelta）
7. 各 rowGroup：
     y -= spinDelta，越界则环绕（无限竖向传送带）
     rotation.y = spinAngle
8. 网格 rotation.y = spinAngle * 0.09        // 稍慢，产生视差
9. Raycaster 悬停 → 目标 scale 1.08
10. 写回每片 uniforms：uBendH/V、uTime
11. renderer.render(scene, camera)
```

### 6.1 输入映射

| 输入 | 效果 |
|------|------|
| `wheel` | `spinTarget -= deltaY * 0.005`，`bendRaw += deltaY * 0.004`（钳制 ±2） |
| 触摸竖直拖动 | 同理，系数略大；松手时追加惯性 |

`bendRaw` 衰减后仍短暂影响 `spinAngle` 增速，所以甩一下会有「冲一下再滑行」的感觉。

### 6.2 竖直环绕

自旋不只绕 Y 转，还把行组沿 Y 平移并用 `±ROWS*rowSpacing/2` 包裹。这样圆柱看起来在**连续滚动**，而不是只转一圈重复同一正面。

---

## 7. 网格背景图

不做封面圆柱上的 `LineSegments`。背景是一张 **Canvas 绘制的网格纹理**，贴在独立的 **内侧开放圆柱**（`CylinderGeometry` + `BackSide`）上：

1. `createGridTexture()`：在 2048×1024 画布上铺底色 `#f3f5fa`，再画细线 / 粗线网格；
2. `ensureBackdrop()`：半径约 32（远大于封面圆柱 ~8）的开放圆柱，`MeshBasicMaterial({ map, side: BackSide })`；
3. 挂在 `scene` 上而非 `rootGroup`，只以 `spinAngle * 0.09` 缓慢跟转，形成轻微视差。

这样网格是「环境墙纸」，不是封面排布几何的一部分。

---

## 8. 交互拾取

```text
pointer → NDC
Raycaster.setFromCamera(ndc, camera)
intersectObjects(panels)
```

- 命中：底部 hover label 显示 `title`，mesh scale → `panelScale * 1.08`
- 滚动/拖拽进行中跳过拾取，避免误触
- 触屏设备关闭 hover 放大（`matchMedia('(hover: none)')`）

---

## 9. 与参考站的关系 / 简化点

本示例忠实复刻了首页圆柱的**主路径**：

- 双布局插值、速度耦合弯曲着色器、行组环绕、网格视差、Raycaster

有意简化、未移植的部分：

| 参考站 | 本示例 |
|--------|--------|
| 中心 `rosa.glb` + MeshPhysical / PMREM | 未加载 GLB |
| 入场 stagger / blur 动画 | 直接可见 |
| 页面过渡 NoSignal / TextDistort | 无 |
| 全局 `distort-canvas`（mooh 式滚动畸变） | 无 |
| Lenis / GSAP | 原生 wheel + RAF |

若要继续对齐参考站，优先加：中心 GLB、入场时间线、以及独立的 distort overlay。

---

## 10. 工程文件索引

| 路径 | 职责 |
|------|------|
| `web/src/views/HomePage.vue` | 首页：拉取 `/api/movies`、随机抽 10 条、Rings/Spiral UI |
| `web/src/components/three/ThreeCylinderScene.vue` | Three.js 场景与着色器 |
| `web/src/router/index.js` | 路由 `/`，`hideChrome: true`；`/demo/cylinder` 重定向到首页 |
| `web/src/App.vue` | 按 `meta.hideChrome` 隐藏壳层 |

本地启动**后端 + 前端**后访问：

```text
http://127.0.0.1:5173/
```

---

## 11. 公式速查

**极坐标放置（混合后）**

$$
\begin{aligned}
\theta &= (1-t)\,\theta_{\mathrm{ring}} + t\,\theta_{\mathrm{spiral}} \\
r &= r_0\bigl(1 + (0.72-1)t\bigr) \\
(x,z) &= (r\cos\theta,\; r\sin\theta) \\
y &= t \cdot y_{\mathrm{spiral}}
\end{aligned}
$$

**面板朝向圆心**

$$
R_y = -(\theta - \pi/2)
$$

**抛物线拱（顶点位移）**

$$
\Delta z = -(1-x_n^2)\,u_{\mathrm{BendH}} - (1-y_n^2)\,u_{\mathrm{BendV}} + \varepsilon_{\mathrm{idle}}
$$

---

## 12. 小结

圆柱画廊的「好看」不主要来自后期特效，而来自三件事叠在一起：

1. **极坐标 + Rings/Spiral 插值** —— 结构清晰、可动画；  
2. **速度驱动的顶点弯曲** —— 运动时有物理感；  
3. **行组环绕 + 差分自转** —— 空间一直在「流动」。

在此基础上换封面纹理、改 `ROWS/COLS/radius`，就可以把同一套机制用到任意内容画廊上。
