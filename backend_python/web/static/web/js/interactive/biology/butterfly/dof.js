import { THREE } from '../../core/engine.js';

const VERT = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';

// Macro-lens depth of field: the scene renders once into a float target, a half-resolution copy is
// blurred in two separable passes, and the composite mixes sharp and blurred pixels by the circle of
// confusion around the focus distance. Low tier skips it entirely and renders straight to the screen.
export function createDof(engine, opts = {}) {
  const { renderer, scene, camera, quality } = engine;
  if (quality.tier === 'low' || !renderer.capabilities.isWebGL2) return null;
  const orig = renderer.render.bind(renderer);
  const msaa = quality.tier === 'high' ? 4 : 0;
  const depthTexture = new THREE.DepthTexture(1, 1);
  depthTexture.type = THREE.UnsignedIntType;
  const main = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: msaa, depthTexture });
  const half = [0, 1].map(() => new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, depthBuffer: false }));
  const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2));
  quad.frustumCulled = false;
  const fsScene = new THREE.Scene();
  fsScene.add(quad);

  const blurMat = new THREE.ShaderMaterial({
    uniforms: { tDiffuse: { value: null }, uDir: { value: new THREE.Vector2() } },
    vertexShader: VERT,
    fragmentShader: `uniform sampler2D tDiffuse; uniform vec2 uDir; varying vec2 vUv;
      void main(){
        vec4 c = texture2D(tDiffuse, vUv) * 0.1964825501511404;
        c += texture2D(tDiffuse, vUv + uDir * 1.411764705882353) * 0.2969069646728344;
        c += texture2D(tDiffuse, vUv - uDir * 1.411764705882353) * 0.2969069646728344;
        c += texture2D(tDiffuse, vUv + uDir * 3.2941176470588234) * 0.09447039785044732;
        c += texture2D(tDiffuse, vUv - uDir * 3.2941176470588234) * 0.09447039785044732;
        c += texture2D(tDiffuse, vUv + uDir * 5.176470588235294) * 0.010381362401148057;
        c += texture2D(tDiffuse, vUv - uDir * 5.176470588235294) * 0.010381362401148057;
        gl_FragColor = c;
      }`,
    depthTest: false, depthWrite: false, toneMapped: false,
  });
  const COC = `#include <packing>
    uniform sampler2D tDepth; uniform float uNear; uniform float uFar; uniform float uFocus; uniform float uAperture;
    float cocAt(vec2 uv) {
      float d = -perspectiveDepthToViewZ(texture2D(tDepth, uv).x, uNear, uFar);
      float c = clamp(abs(d - uFocus) / (uFocus * 0.9 + 0.001) * uAperture, 0.0, 1.0);
      return smoothstep(0.18, 0.95, c);
    }`;
  const lens = { uNear: { value: 0.1 }, uFar: { value: 1000 }, uFocus: { value: 10 }, uAperture: { value: opts.aperture ?? 1 }, tDepth: { value: depthTexture } };
  const copyMat = new THREE.ShaderMaterial({
    uniforms: { tDiffuse: { value: null }, ...lens },
    vertexShader: VERT,
    fragmentShader: `${COC}
      uniform sampler2D tDiffuse; varying vec2 vUv;
      void main(){ float c = max(cocAt(vUv), 0.02); gl_FragColor = vec4(texture2D(tDiffuse, vUv).rgb * c, c); }`,
    depthTest: false, depthWrite: false, toneMapped: false,
  });
  const compMat = new THREE.ShaderMaterial({
    uniforms: {
      tSharp: { value: main.texture }, tBlur: { value: half[0].texture }, ...lens,
      uVignette: { value: opts.vignette ?? 0.22 },
    },
    vertexShader: VERT,
    fragmentShader: `${COC}
      uniform sampler2D tSharp; uniform sampler2D tBlur; uniform float uVignette;
      varying vec2 vUv;
      void main(){
        float coc = cocAt(vUv);
        vec4 s = texture2D(tSharp, vUv);
        vec4 b = texture2D(tBlur, vUv);
        vec3 bc = b.rgb / max(b.a, 0.0001);
        vec3 col = mix(s.rgb, bc, coc);
        vec2 q = vUv - 0.5;
        col *= 1.0 - uVignette * dot(q, q) * 2.2;
        gl_FragColor = vec4(col, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
    depthTest: false, depthWrite: false,
  });

  let enabled = opts.enabled !== false;
  let focus = 10;
  const size = new THREE.Vector2();
  function resize() {
    renderer.getDrawingBufferSize(size);
    main.setSize(size.x, size.y);
    depthTexture.image.width = size.x; depthTexture.image.height = size.y;
    const hw = Math.max(1, Math.round(size.x / 2)); const hh = Math.max(1, Math.round(size.y / 2));
    half.forEach((r) => r.setSize(hw, hh));
  }
  resize();
  let lastW = 0; let lastH = 0;

  function pass(mat, target) {
    quad.material = mat;
    renderer.setRenderTarget(target);
    orig(fsScene, ortho);
  }

  renderer.render = (s, c) => {
    if (s !== scene || !enabled) { orig(s, c); return; }
    renderer.getDrawingBufferSize(size);
    if (size.x !== lastW || size.y !== lastH) { lastW = size.x; lastH = size.y; resize(); }
    const prev = renderer.getRenderTarget();
    renderer.setRenderTarget(main);
    orig(s, c);
    lens.uNear.value = camera.near; lens.uFar.value = camera.far; lens.uFocus.value = focus;
    copyMat.uniforms.tDiffuse.value = main.texture;
    pass(copyMat, half[0]);
    const hw = half[0].width; const hh = half[0].height;
    for (let i = 0; i < 2; i++) {
      blurMat.uniforms.tDiffuse.value = half[0].texture; blurMat.uniforms.uDir.value.set(1.6 / hw, 0); pass(blurMat, half[1]);
      blurMat.uniforms.tDiffuse.value = half[1].texture; blurMat.uniforms.uDir.value.set(0, 1.6 / hh); pass(blurMat, half[0]);
    }
    pass(compMat, prev);
  };

  return {
    set focus(v) { focus = v; },
    set aperture(v) { lens.uAperture.value = v; },
    set enabled(v) { enabled = v; },
    dispose() {
      renderer.render = orig;
      main.dispose(); half.forEach((r) => r.dispose()); depthTexture.dispose();
      blurMat.dispose(); copyMat.dispose(); compMat.dispose(); quad.geometry.dispose();
    },
  };
}
