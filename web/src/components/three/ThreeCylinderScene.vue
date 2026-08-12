<template>
  <div class="cylinder-scene">
    <canvas ref="canvasRef" class="cylinder-canvas" />
    <div v-if="hoveredTitle" class="hover-label">{{ hoveredTitle }}</div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as THREE from 'three'

const props = defineProps({
  projects: {
    type: Array,
    default: () => [],
  },
  spiral: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['hover-project', 'open-project'])

const ROWS = 5
const COLS = 12
const PANEL_SCALE = 1.1
const PANEL_ASPECT = 16 / 9
const SPIRAL_RADIUS_FACTOR = 0.72
const BEND_V_MAX = 0.25
const BEND_H_MAX = 0.15
const ROW_SEEDS = [0x91a2b3c4, 0x11c0ffee, 0x55aa33dd, 0x7e1d2c3b, 0xabcdef01]

const LINEAR_TO_SRGB = `
  vec3 linearToSRGB(vec3 c) { return pow(max(c, 0.0), vec3(1.0 / 2.2)); }
`

const PANEL_VERT = `
  uniform float uBendH;
  uniform float uBendV;
  uniform float uTime;
  uniform float uPhase;
  varying vec2  vUv;
  varying float vViewZ;

  void main() {
    vUv = uv;
    vec3 pos = position;

    float xn = (uv.x - 0.5) * 2.0;
    float yn = (uv.y - 0.5) * 2.0;
    float archX = 1.0 - xn * xn;
    float archY = 1.0 - yn * yn;

    pos.z -= archX * uBendH;
    pos.z -= archY * uBendV;
    pos.z += sin(uv.y * 6.283 + uTime * 0.55 + uPhase)
           * sin(uv.x * 3.14  + uTime * 0.35 + uPhase * 1.3) * 0.016;

    vec4 mvPos = modelViewMatrix * vec4(pos, 1.0);
    vViewZ = -mvPos.z;
    gl_Position = projectionMatrix * mvPos;
  }
`

const PANEL_FRAG = `
  uniform sampler2D uTexture;
  uniform float     uOpacity;
  uniform float     uBlur;
  uniform float     uDepthNear;
  uniform float     uDepthFar;
  uniform vec3      uDepthColor;
  uniform float     uDepthStrength;
  varying vec2      vUv;
  varying float     vViewZ;

  ${LINEAR_TO_SRGB}

  vec4 sampleBlurred(sampler2D tex, vec2 uv, float blur) {
    if (blur <= 0.0005) return texture2D(tex, uv);
    vec4 acc  = texture2D(tex, uv) * 0.25;
    acc      += texture2D(tex, uv + vec2( blur, 0.0))   * 0.125;
    acc      += texture2D(tex, uv + vec2(-blur, 0.0))   * 0.125;
    acc      += texture2D(tex, uv + vec2(0.0,   blur))  * 0.125;
    acc      += texture2D(tex, uv + vec2(0.0,  -blur))  * 0.125;
    acc      += texture2D(tex, uv + vec2( blur,  blur)) * 0.0625;
    acc      += texture2D(tex, uv + vec2(-blur,  blur)) * 0.0625;
    acc      += texture2D(tex, uv + vec2( blur, -blur)) * 0.0625;
    acc      += texture2D(tex, uv + vec2(-blur, -blur)) * 0.0625;
    return acc;
  }

  void main() {
    vec4 col = sampleBlurred(uTexture, vUv, uBlur);
    float depthT = smoothstep(uDepthNear, uDepthFar, vViewZ);
    float luma   = dot(col.rgb, vec3(0.2126, 0.7152, 0.0722));
    vec3  toned  = mix(col.rgb, vec3(luma), depthT * 0.12);
    toned        = mix(toned, uDepthColor, depthT * uDepthStrength);
    col.rgb      = linearToSRGB(toned);
    col.a    *= uOpacity;
    gl_FragColor = col;
  }
`

const canvasRef = ref(null)
const hoveredTitle = ref('')

let renderer
let scene
let camera
let rootGroup
let backdrop
let gridTexture
let rowGroups = []
let panels = []
let sharedGeometry
let raf = 0
let disposed = false

let spiralBlend = 0
let spiralTarget = 0
let radiusBase = 7.8
let rowSpacing = 7
let panelScale = 1

let spinTarget = 0
let spinSmooth = 0
let spinPrev = 0
let spinAngle = 0
let bendRaw = 0
let bendV = 0
let bendH = 0
let elapsed = 0
let lastTs = 0

let pointerNdc = new THREE.Vector2(2, 2)
let raycaster = new THREE.Raycaster()
let hoveredMesh = null
let isTouch = false
let scrollingUi = false
let scrollUiTimer = 0

const textureCache = new Map()
const textureLoader = new THREE.TextureLoader()
textureLoader.crossOrigin = 'anonymous'

function mulberry32(seed) {
  let t = seed >>> 0
  return () => {
    t = (t + 0x6d2b79f5) >>> 0
    let r = t
    r = Math.imul(r ^ (r >>> 15), r | 1)
    r ^= r + Math.imul(r ^ (r >>> 7), r | 61)
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296
  }
}

function shuffle(list, seed) {
  const arr = [...list]
  const rand = mulberry32(seed)
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr
}

function layoutParams() {
  const w = window.innerWidth
  const tall = window.innerHeight > w
  // 影片封面按横版 16:9；baseH 为面板高度，宽度 = height × 16/9
  const size = (baseH, extras) => ({
    ...extras,
    panelW: baseH * PANEL_ASPECT * PANEL_SCALE,
    panelH: baseH * PANEL_SCALE,
  })

  if (w < 768 && !tall) {
    return size(1.15, { fov: 50, cameraZ: 13, radius: 7.8, rowSpacing: 4.6 })
  }
  if (w < 500) {
    return size(0.85, { fov: 70, cameraZ: 7.5, radius: 4.5, rowSpacing: 3.4 })
  }
  if (w < 768) {
    return size(0.9, { fov: 70, cameraZ: 9.5, radius: 4.6, rowSpacing: 3.2 })
  }
  if (w < 1024 && tall) {
    return size(0.95, { fov: 65, cameraZ: 9, radius: 5.5, rowSpacing: 4.2 })
  }
  if (w < 1024) {
    return size(1.05, { fov: 60, cameraZ: 11, radius: 6.5, rowSpacing: 3.6 })
  }
  return size(1.2, { fov: 50, cameraZ: 13, radius: 7.8, rowSpacing: 4.8 })
}

function loadTexture(url) {
  if (!url) return null
  if (textureCache.has(url)) return textureCache.get(url)
  const tex = textureLoader.load(url)
  tex.colorSpace = THREE.SRGBColorSpace
  tex.minFilter = THREE.LinearMipmapLinearFilter
  tex.magFilter = THREE.LinearFilter
  textureCache.set(url, tex)
  return tex
}

/** 绘制网格背景图（Canvas → Texture），贴在内侧大圆柱上，不挂在封面圆柱几何上 */
function createGridTexture() {
  const width = 2048
  const height = 1024
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')

  ctx.fillStyle = '#f3f5fa'
  ctx.fillRect(0, 0, width, height)

  const cell = 64
  const majorEvery = 4

  ctx.strokeStyle = 'rgba(122, 132, 168, 0.2)'
  ctx.lineWidth = 1
  for (let x = 0; x <= width; x += cell) {
    ctx.beginPath()
    ctx.moveTo(x + 0.5, 0)
    ctx.lineTo(x + 0.5, height)
    ctx.stroke()
  }
  for (let y = 0; y <= height; y += cell) {
    ctx.beginPath()
    ctx.moveTo(0, y + 0.5)
    ctx.lineTo(width, y + 0.5)
    ctx.stroke()
  }

  ctx.strokeStyle = 'rgba(90, 100, 140, 0.36)'
  ctx.lineWidth = 1.5
  for (let x = 0; x <= width; x += cell * majorEvery) {
    ctx.beginPath()
    ctx.moveTo(x + 0.5, 0)
    ctx.lineTo(x + 0.5, height)
    ctx.stroke()
  }
  for (let y = 0; y <= height; y += cell * majorEvery) {
    ctx.beginPath()
    ctx.moveTo(0, y + 0.5)
    ctx.lineTo(width, y + 0.5)
    ctx.stroke()
  }

  const texture = new THREE.CanvasTexture(canvas)
  texture.colorSpace = THREE.SRGBColorSpace
  texture.anisotropy = 8
  texture.wrapS = THREE.RepeatWrapping
  texture.wrapT = THREE.ClampToEdgeWrapping
  texture.needsUpdate = true
  return texture
}

function ensureBackdrop() {
  if (!scene || backdrop) return

  gridTexture = createGridTexture()
  // 开放圆柱：相机在内部看 BackSide，形成环绕网格墙纸
  const geometry = new THREE.CylinderGeometry(32, 32, 64, 72, 1, true)
  const material = new THREE.MeshBasicMaterial({
    map: gridTexture,
    side: THREE.BackSide,
    depthWrite: false,
    toneMapped: false,
  })
  backdrop = new THREE.Mesh(geometry, material)
  backdrop.renderOrder = -100
  backdrop.frustumCulled = false
  scene.add(backdrop)
}

function disposeBackdrop() {
  if (backdrop) {
    scene?.remove(backdrop)
    backdrop.geometry?.dispose()
    backdrop.material?.dispose()
    backdrop = null
  }
  if (gridTexture) {
    gridTexture.dispose()
    gridTexture = null
  }
}

function applyLayoutBlend(t) {
  const radius = radiusBase * (1 + (SPIRAL_RADIUS_FACTOR - 1) * t)
  const mobileLandscape =
    isTouch && window.innerWidth < 768 && window.innerHeight > window.innerWidth
  panelScale = 1 + ((mobileLandscape ? 0.88 : 1.26) - 1) * t

  for (const mesh of panels) {
    const { thetaRing, thetaSpiral, ySpiral } = mesh.userData
    const theta = thetaRing + (thetaSpiral - thetaRing) * t
    mesh.position.x = Math.cos(theta) * radius
    mesh.position.z = Math.sin(theta) * radius
    mesh.position.y = ySpiral * t
    mesh.rotation.y = -(theta - Math.PI / 2)
  }
}

function clearPanels() {
  for (const group of rowGroups) {
    rootGroup.remove(group)
    for (const child of group.children) {
      child.material?.dispose?.()
    }
  }
  rowGroups = []
  panels = []
  if (sharedGeometry) {
    sharedGeometry.dispose()
    sharedGeometry = null
  }
}

function rebuildPanels() {
  const list = props.projects.filter((p) => p?.cover || p?.image)
  if (!list.length || !rootGroup) return

  clearPanels()
  const layout = layoutParams()
  radiusBase = layout.radius
  rowSpacing = layout.rowSpacing

  const depthNear = layout.cameraZ * 0.58
  const depthFar = layout.cameraZ * 1.85
  const depthColor = new THREE.Color(0xc5cde0).convertSRGBToLinear()

  sharedGeometry = new THREE.PlaneGeometry(layout.panelW, layout.panelH, 12, 8)

  for (let row = 0; row < ROWS; row += 1) {
    const group = new THREE.Group()
    const shuffled = shuffle(list, ROW_SEEDS[row] ?? row * 9973)

    for (let col = 0; col < COLS; col += 1) {
      const project = shuffled[col % shuffled.length]
      const cover = project.cover || project.image
      const material = new THREE.ShaderMaterial({
        uniforms: {
          uTexture: { value: loadTexture(cover) },
          uBendH: { value: 0 },
          uBendV: { value: 0 },
          uTime: { value: 0 },
          uPhase: { value: Math.random() * Math.PI * 2 },
          uOpacity: { value: 1 },
          uBlur: { value: 0 },
          uDepthNear: { value: depthNear },
          uDepthFar: { value: depthFar },
          uDepthColor: { value: depthColor },
          uDepthStrength: { value: 0.22 },
        },
        vertexShader: PANEL_VERT,
        fragmentShader: PANEL_FRAG,
        side: THREE.DoubleSide,
        transparent: false,
        depthWrite: true,
        toneMapped: false,
      })

      const mesh = new THREE.Mesh(sharedGeometry, material)
      mesh.frustumCulled = false
      mesh.userData = {
        ...project,
        isInteractive: true,
        thetaRing: ((col + row * 0.5) / COLS) * Math.PI * 2,
        thetaSpiral: (col / COLS) * Math.PI * 2,
        ySpiral: (col / COLS - 0.5) * layout.rowSpacing,
        targetScale: 1,
      }
      group.add(mesh)
    }

    group.position.y = row * layout.rowSpacing - ((ROWS - 1) * layout.rowSpacing) / 2
    rowGroups.push(group)
    rootGroup.add(group)
  }

  panels = rowGroups.flatMap((g) => g.children)
  spiralTarget = props.spiral ? 1 : 0
  spiralBlend = spiralTarget
  applyLayoutBlend(spiralBlend)
  panels.forEach((mesh) => mesh.scale.setScalar(panelScale))
}

function markUiScroll() {
  scrollingUi = true
  clearTimeout(scrollUiTimer)
  scrollUiTimer = setTimeout(() => {
    scrollingUi = false
  }, 200)
}

function onWheel(event) {
  spinTarget -= event.deltaY * 0.005
  bendRaw += event.deltaY * 0.004
  bendRaw = Math.max(-2, Math.min(2, bendRaw))
  markUiScroll()
}

function onPointerMove(event) {
  const canvas = canvasRef.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  pointerNdc.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  pointerNdc.y = -((event.clientY - rect.top) / rect.height) * 2 + 1
}

function projectPayload(mesh) {
  if (!mesh?.userData) return null
  const { id, title, cover, rating, image } = mesh.userData
  if (!id) return null
  return { id, title, cover: cover || image, rating }
}

function pickMeshAtClient(clientX, clientY) {
  const canvas = canvasRef.value
  if (!canvas || !camera || !panels.length) return null
  const rect = canvas.getBoundingClientRect()
  if (
    clientX < rect.left ||
    clientX > rect.right ||
    clientY < rect.top ||
    clientY > rect.bottom
  ) {
    return null
  }
  const ndc = new THREE.Vector2(
    ((clientX - rect.left) / rect.width) * 2 - 1,
    -((clientY - rect.top) / rect.height) * 2 + 1,
  )
  raycaster.setFromCamera(ndc, camera)
  const hits = raycaster.intersectObjects(panels, false)
  return hits[0]?.object || null
}

function onClick(event) {
  if (isTouch || scrollingUi) return
  const canvas = canvasRef.value
  if (!canvas || event.target !== canvas) return

  const mesh = pickMeshAtClient(event.clientX, event.clientY) || hoveredMesh
  const payload = projectPayload(mesh)
  if (!payload) return
  emit('open-project', payload)
}

let touchStartY = 0
let touchDeltaY = 0
let touchMoved = false
let touchLastX = 0
let touchLastY = 0

function onTouchStart(event) {
  const touch = event.touches?.[0]
  if (!touch) return
  touchStartY = touch.clientY
  touchLastX = touch.clientX
  touchLastY = touch.clientY
  touchDeltaY = 0
  touchMoved = false
}

function onTouchMove(event) {
  const touch = event.touches?.[0]
  if (!touch) return
  const dy = touchStartY - touch.clientY
  touchDeltaY = dy
  if (Math.abs(dy) > 10) touchMoved = true
  spinTarget -= dy * 0.008
  bendRaw += dy * 0.007
  bendRaw = Math.max(-2, Math.min(2, bendRaw))
  touchStartY = touch.clientY
  touchLastX = touch.clientX
  touchLastY = touch.clientY
  markUiScroll()
}

function onTouchEnd(event) {
  if (!touchMoved) {
    const touch = event.changedTouches?.[0]
    const x = touch?.clientX ?? touchLastX
    const y = touch?.clientY ?? touchLastY
    const mesh = pickMeshAtClient(x, y)
    const payload = projectPayload(mesh)
    if (payload) emit('open-project', payload)
  } else {
    spinTarget -= touchDeltaY * 0.008 * 3.5
    bendRaw += touchDeltaY * 0.007 * 3.5
    bendRaw = Math.max(-2, Math.min(2, bendRaw))
  }
}

function onResize() {
  if (!camera || !renderer || !canvasRef.value) return
  const layout = layoutParams()
  const { clientWidth: w, clientHeight: h } = canvasRef.value.parentElement || canvasRef.value
  camera.fov = layout.fov
  camera.position.z = layout.cameraZ
  camera.aspect = w / Math.max(h, 1)
  camera.updateProjectionMatrix()
  renderer.setSize(w, h, false)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
  rebuildPanels()
}

function tick(now) {
  raf = requestAnimationFrame(tick)
  if (!renderer || !scene || !camera) return

  const dt = Math.min((now - lastTs) / 1000, 0.05)
  lastTs = now
  elapsed += dt

  if (Math.abs(spiralTarget - spiralBlend) > 1e-4) {
    spiralBlend += (spiralTarget - spiralBlend) * (1 - Math.exp(-3.2 * dt))
    if (Math.abs(spiralTarget - spiralBlend) <= 1e-4) spiralBlend = spiralTarget
    applyLayoutBlend(spiralBlend)
  }

  spinSmooth += (spinTarget - spinSmooth) * 0.1
  const spinDelta = spinSmooth - spinPrev
  spinPrev = spinSmooth

  bendRaw *= Math.pow(0.92, dt * 60)
  spinAngle += (0.08 + bendRaw) * dt
  bendV += (THREE.MathUtils.clamp(bendRaw * 0.1, -BEND_V_MAX, BEND_V_MAX) - bendV) * 0.08
  bendH += (THREE.MathUtils.clamp(spinDelta * 8, -BEND_H_MAX, BEND_H_MAX) - bendH) * 0.12

  const wrapSpan = ROWS * rowSpacing
  for (const group of rowGroups) {
    group.position.y -= spinDelta
    if (group.position.y > wrapSpan / 2 + rowSpacing) group.position.y -= wrapSpan
    if (group.position.y < -wrapSpan / 2 - rowSpacing) group.position.y += wrapSpan
    group.rotation.y = spinAngle
  }
  if (backdrop) backdrop.rotation.y = spinAngle * 0.09

  let hit = null
  if (!scrollingUi && !isTouch && panels.length) {
    raycaster.setFromCamera(pointerNdc, camera)
    const intersects = raycaster.intersectObjects(panels, false)
    hit = intersects[0]?.object || null
  }

  if (hit !== hoveredMesh) {
    hoveredMesh = hit
    hoveredTitle.value = hit?.userData?.title || ''
    emit('hover-project', hit ? projectPayload(hit) : null)
    if (canvasRef.value) {
      canvasRef.value.style.cursor = hit ? 'pointer' : 'default'
    }
  }

  const hoverLerp = 1 - Math.exp(-8 * dt)
  for (const mesh of panels) {
    const hoverBoost = !isTouch && hit === mesh ? 1.08 : 1
    const target = panelScale * hoverBoost
    mesh.scale.setScalar(mesh.scale.x + (target - mesh.scale.x) * hoverLerp)
    const uniforms = mesh.material.uniforms
    uniforms.uBendH.value = bendH
    uniforms.uBendV.value = bendV
    uniforms.uTime.value = elapsed
  }

  renderer.render(scene, camera)
}

function init() {
  const canvas = canvasRef.value
  if (!canvas) return

  isTouch = window.matchMedia('(hover: none)').matches
  const parent = canvas.parentElement
  const w = parent?.clientWidth || window.innerWidth
  const h = parent?.clientHeight || window.innerHeight
  const layout = layoutParams()

  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xf3f5fa)

  camera = new THREE.PerspectiveCamera(layout.fov, w / Math.max(h, 1), 0.1, 200)
  camera.position.set(0, 0, layout.cameraZ)

  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false })
  renderer.setSize(w, h, false)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.toneMapping = THREE.NoToneMapping

  rootGroup = new THREE.Group()
  scene.add(rootGroup)
  scene.add(new THREE.AmbientLight(0xffffff, 0.35))
  const key = new THREE.DirectionalLight(0xffffff, 0.8)
  key.position.set(4, 6, 8)
  scene.add(key)

  ensureBackdrop()
  rebuildPanels()

  window.addEventListener('wheel', onWheel, { passive: true })
  window.addEventListener('resize', onResize)
  window.addEventListener('mousemove', onPointerMove, { passive: true })
  window.addEventListener('click', onClick)
  window.addEventListener('touchstart', onTouchStart, { passive: true })
  window.addEventListener('touchmove', onTouchMove, { passive: true })
  window.addEventListener('touchend', onTouchEnd, { passive: true })

  lastTs = performance.now()
  raf = requestAnimationFrame(tick)
}

function dispose() {
  disposed = true
  cancelAnimationFrame(raf)
  clearTimeout(scrollUiTimer)
  window.removeEventListener('wheel', onWheel)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('mousemove', onPointerMove)
  window.removeEventListener('click', onClick)
  window.removeEventListener('touchstart', onTouchStart)
  window.removeEventListener('touchmove', onTouchMove)
  window.removeEventListener('touchend', onTouchEnd)

  clearPanels()
  disposeBackdrop()
  for (const tex of textureCache.values()) tex.dispose()
  textureCache.clear()
  renderer?.dispose()
  renderer = null
  scene = null
  camera = null
  rootGroup = null
}

watch(
  () => props.projects,
  () => {
    if (!disposed && scene) rebuildPanels()
  },
  { deep: false },
)

watch(
  () => props.spiral,
  (value) => {
    spiralTarget = value ? 1 : 0
  },
)

onMounted(() => {
  disposed = false
  init()
})

onBeforeUnmount(() => {
  dispose()
})
</script>

<style scoped>
.cylinder-scene {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #f3f5fa;
}

.cylinder-canvas {
  display: block;
  width: 100%;
  height: 100%;
  touch-action: none;
}

.hover-label {
  position: absolute;
  left: 50%;
  bottom: 48px;
  transform: translateX(-50%);
  padding: 10px 18px;
  border-radius: 999px;
  background: rgba(21, 0, 225, 0.9);
  color: #fff;
  font-size: 14px;
  letter-spacing: 0.02em;
  pointer-events: none;
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 24px rgba(21, 0, 225, 0.18);
}
</style>
