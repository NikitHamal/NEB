package com.neb.ians.ui.sim.gl

import android.opengl.GLES30
import android.opengl.GLSurfaceView
import android.opengl.Matrix
import android.util.Log
import javax.microedition.khronos.egl.EGLConfig
import javax.microedition.khronos.opengles.GL10

/** What a native 3D simulation implements. Called on the GL thread, under the scene lock. */
abstract class GlSim {
    /** Builds the scene once (meshes upload lazily on first draw). */
    open fun build(scene: GlScene) {}
    /** Advances the simulation by dt seconds. */
    open fun step(dt: Float, scene: GlScene) {}
    /** A press: return true to take the gesture (dragging an object) instead of orbiting. */
    open fun pointerDown(origin: FloatArray, dir: FloatArray): Boolean = false
    open fun pointerMove(origin: FloatArray, dir: FloatArray) {}
    open fun pointerUp() {}
    /** Whether something is moving; an idle scene drops to a few frames a second. */
    open val animating: Boolean get() = true
}

private const val VS = """#version 300 es
layout(location=0) in vec3 aPos; layout(location=1) in vec3 aNor;
uniform mat4 uModel; uniform mat4 uVP; uniform mat4 uNormal;
out vec3 vW; out vec3 vN; out vec3 vL;
void main(){ vec4 w=uModel*vec4(aPos,1.0); vW=w.xyz; vL=aPos; vN=mat3(uNormal)*aNor; gl_Position=uVP*w; }"""

private const val FS = """#version 300 es
precision highp float;
in vec3 vW; in vec3 vN; in vec3 vL; out vec4 o;
uniform vec3 uColor; uniform float uRough; uniform float uMetal; uniform float uEmis; uniform float uAlpha; uniform int uUnlit;
uniform vec3 uEye; uniform vec3 uKey; uniform vec3 uSkyTop; uniform vec3 uSkyBot; uniform vec3 uGround; uniform float uKeyI; uniform float uExposure; uniform float uFade;
vec3 aces(vec3 x){ return clamp((x*(2.51*x+0.03))/(x*(2.43*x+0.59)+0.14),0.0,1.0); }
void main(){
  vec3 base=uColor; float alpha=uAlpha;
  if(uFade>0.0){ alpha*=1.0-smoothstep(uFade*0.45,uFade,length(vW.xz)); }
  if(uUnlit==1){ o=vec4(pow(aces(base*uExposure*(1.0+uEmis)),vec3(1.0/2.2)),alpha); return; }
  vec3 N=normalize(vN); vec3 V=normalize(uEye-vW); if(dot(N,V)<0.0) N=-N;
  vec3 L=normalize(uKey); vec3 H=normalize(L+V);
  float NL=max(dot(N,L),0.0); float NH=max(dot(N,H),0.0); float NV=max(dot(N,V),1e-3); float VH=max(dot(V,H),0.0);
  float r=clamp(uRough,0.04,1.0); float a=r*r; float a2=a*a;
  float d=NH*NH*(a2-1.0)+1.0; float D=a2/(3.14159*d*d);
  float k=(r+1.0)*(r+1.0)/8.0; float G=(NL/(NL*(1.0-k)+k))*(NV/(NV*(1.0-k)+k));
  vec3 F0=mix(vec3(0.04),base,uMetal); vec3 F=F0+(1.0-F0)*pow(1.0-VH,5.0);
  vec3 spec=D*G*F/(4.0*NL*NV+1e-3);
  vec3 kd=(1.0-F)*(1.0-uMetal);
  vec3 direct=(kd*base/3.14159+spec)*NL*uKeyI;
  float up=N.y*0.5+0.5; vec3 amb=mix(uGround*0.8,uSkyTop,up);
  vec3 R=reflect(-V,N); float ry=R.y*0.5+0.5;
  vec3 env=mix(uGround*0.7,mix(uSkyBot,uSkyTop,ry),smoothstep(0.38,0.62,ry));
  env+=vec3(3.0)*pow(max(dot(R,normalize(vec3(-0.45,0.85,0.55))),0.0),2.0+80.0*(1.0-r)*(1.0-r));
  vec3 Fa=F0+(max(vec3(1.0-r),F0)-F0)*pow(1.0-NV,5.0);
  vec3 c=direct+kd*base*amb+env*Fa*(1.0-r*0.6)+base*uEmis;
  o=vec4(pow(aces(c*uExposure),vec3(1.0/2.2)),alpha);
}"""

private const val BG_VS = """#version 300 es
out vec2 vUv; void main(){ vec2 p=vec2(float((gl_VertexID<<1)&2),float(gl_VertexID&2)); vUv=p; gl_Position=vec4(p*2.0-1.0,0.9999,1.0); }"""
private const val BG_FS = """#version 300 es
precision mediump float; in vec2 vUv; out vec4 o; uniform vec3 uTop; uniform vec3 uBot;
void main(){ float t=clamp(vUv.y,0.0,1.0); vec3 c=mix(uBot,uTop,smoothstep(0.0,1.0,t)); float v=distance(vUv,vec2(0.5,0.45)); c*=1.0-0.18*v*v; o=vec4(c,1.0); }"""
private const val BLOB_FS = """#version 300 es
precision mediump float; in vec3 vW; in vec3 vN; in vec3 vL; out vec4 o; uniform float uAlpha;
void main(){ float r=clamp(length(vL.xz),0.0,1.0); float a=uAlpha*pow(1.0-r*r,2.2); o=vec4(0.05,0.07,0.12,a); }"""

/**
 * Draws a [GlScene]: a gradient backdrop, a fading studio floor, soft contact shadows, opaque
 * then transparent nodes with a physically based shader (GGX specular, hemisphere ambient, a
 * studio-sky reflection with a softbox highlight, ACES tone mapping). Idle scenes throttle.
 */
class GlRenderer(private val sim: GlSim, val scene: GlScene, private val lowEnd: Boolean) : GLSurfaceView.Renderer {
    private var prog = 0; private var bgProg = 0; private var blobProg = 0
    private val u = HashMap<String, Int>()
    private var built = false
    private var last = 0L
    private var aspect = 1f
    @Volatile var dragging = false
    private val normal = FloatArray(16); private val tmp = FloatArray(16)
    private val ground = GlMesh.disc(1f, 64)
    private val blob = GlMesh.disc(1f, 32)
    private val groundMat = GlMaterial(0xE9ECF1, roughness = 0.92f)
    private val transparent = ArrayList<GlNode>()
    private val meshes = HashSet<GlMesh>()

    override fun onSurfaceCreated(gl: GL10?, config: EGLConfig?) {
        prog = program(VS, FS); bgProg = program(BG_VS, BG_FS); blobProg = program(VS, BLOB_FS)
        u.clear()
        // the context is new: any mesh uploaded to an old one must upload again
        ground.invalidate(); blob.invalidate(); meshes.forEach { it.invalidate() }
        synchronized(scene) { if (!built) { sim.build(scene); built = true } }
        GLES30.glEnable(GLES30.GL_DEPTH_TEST)
        GLES30.glDisable(GLES30.GL_CULL_FACE)
        last = System.nanoTime()
    }

    override fun onSurfaceChanged(gl: GL10?, width: Int, height: Int) {
        GLES30.glViewport(0, 0, width, height)
        aspect = width.toFloat() / height.coerceAtLeast(1)
    }

    override fun onDrawFrame(gl: GL10?) {
        val now = System.nanoTime()
        var dt = ((now - last) / 1e9f).coerceIn(0f, 0.05f)
        val minFrame = if (lowEnd) 0.031f else 0f
        if (dt < minFrame) { try { Thread.sleep(((minFrame - dt) * 1000).toLong()) } catch (_: InterruptedException) {} ; dt = minFrame }
        last = System.nanoTime()
        synchronized(scene) {
            sim.step(dt, scene)
            scene.camera.update(dt, aspect, dragging)
            scene.root.update(null)
            draw()
        }
    }

    private fun loc(p: Int, name: String): Int = u.getOrPut("$p:$name") { GLES30.glGetUniformLocation(p, name) }

    private fun draw() {
        GLES30.glClear(GLES30.GL_COLOR_BUFFER_BIT or GLES30.GL_DEPTH_BUFFER_BIT)
        // backdrop
        GLES30.glDepthMask(false)
        GLES30.glUseProgram(bgProg)
        setSrgb(loc(bgProg, "uTop"), scene.skyTop); setSrgb(loc(bgProg, "uBot"), scene.skyBottom)
        GLES30.glBindVertexArray(0)
        GLES30.glDrawArrays(GLES30.GL_TRIANGLES, 0, 3)
        GLES30.glDepthMask(true)

        GLES30.glUseProgram(prog)
        val cam = scene.camera
        GLES30.glUniformMatrix4fv(loc(prog, "uVP"), 1, false, cam.viewProj, 0)
        GLES30.glUniform3f(loc(prog, "uEye"), cam.eye[0], cam.eye[1], cam.eye[2])
        GLES30.glUniform3f(loc(prog, "uKey"), scene.keyDir[0], scene.keyDir[1], scene.keyDir[2])
        GLES30.glUniform1f(loc(prog, "uKeyI"), scene.keyIntensity)
        GLES30.glUniform1f(loc(prog, "uExposure"), scene.exposure)
        setLinear(loc(prog, "uSkyTop"), scene.skyTop); setLinear(loc(prog, "uSkyBot"), scene.skyBottom); setLinear(loc(prog, "uGround"), scene.groundColor)

        GLES30.glEnable(GLES30.GL_BLEND)
        GLES30.glBlendFunc(GLES30.GL_SRC_ALPHA, GLES30.GL_ONE_MINUS_SRC_ALPHA)
        if (scene.showGround) {
            groundMat.setColor(scene.groundColor)
            Matrix.setIdentityM(tmp, 0); Matrix.translateM(tmp, 0, cam.target[0], scene.groundY, cam.target[2]); Matrix.scaleM(tmp, 0, 30f, 1f, 30f)
            GLES30.glUniform1f(loc(prog, "uFade"), 30f)
            drawMesh(prog, ground, groundMat, tmp)
            GLES30.glUniform1f(loc(prog, "uFade"), 0f)
        }
        // contact shadows
        GLES30.glDepthMask(false)
        GLES30.glUseProgram(blobProg)
        GLES30.glUniformMatrix4fv(loc(blobProg, "uVP"), 1, false, cam.viewProj, 0)
        forEachVisible(scene.root) { n ->
            if (n.blobShadow > 0f) {
                val h = (n.world[13] - scene.groundY).coerceAtLeast(0f)
                val r = n.blobShadow * (1f + h * 0.25f)
                Matrix.setIdentityM(tmp, 0); Matrix.translateM(tmp, 0, n.world[12], scene.groundY + 0.003f, n.world[14]); Matrix.scaleM(tmp, 0, r, 1f, r)
                GLES30.glUniform1f(loc(blobProg, "uAlpha"), (0.42f / (1f + h * 0.8f)))
                GLES30.glUniformMatrix4fv(loc(blobProg, "uModel"), 1, false, tmp, 0)
                blob.bind(); GLES30.glDrawElements(GLES30.GL_TRIANGLES, blob.count, GLES30.GL_UNSIGNED_INT, 0)
            }
        }
        GLES30.glDepthMask(true)
        GLES30.glUseProgram(prog)
        // opaque, then transparent back to front
        transparent.clear()
        forEachVisible(scene.root) { n ->
            val m = n.mesh ?: return@forEachVisible; val mat = n.material ?: return@forEachVisible
            meshes.add(m)
            if (mat.alpha < 1f) transparent.add(n) else drawMesh(prog, m, mat, n.world)
        }
        if (transparent.isNotEmpty()) {
            val e = cam.eye
            transparent.sortByDescending { n -> val dx = n.world[12] - e[0]; val dy = n.world[13] - e[1]; val dz = n.world[14] - e[2]; dx * dx + dy * dy + dz * dz }
            GLES30.glDepthMask(false)
            for (n in transparent) drawMesh(prog, n.mesh!!, n.material!!, n.world)
            GLES30.glDepthMask(true)
        }
        GLES30.glDisable(GLES30.GL_BLEND)
        GLES30.glBindVertexArray(0)
    }

    private fun drawMesh(p: Int, m: GlMesh, mat: GlMaterial, model: FloatArray) {
        GLES30.glUniformMatrix4fv(loc(p, "uModel"), 1, false, model, 0)
        Matrix.invertM(normal, 0, model, 0); Matrix.transposeM(tmp2, 0, normal, 0)
        GLES30.glUniformMatrix4fv(loc(p, "uNormal"), 1, false, tmp2, 0)
        GLES30.glUniform3f(loc(p, "uColor"), mat.rgb[0], mat.rgb[1], mat.rgb[2])
        GLES30.glUniform1f(loc(p, "uRough"), mat.roughness)
        GLES30.glUniform1f(loc(p, "uMetal"), mat.metalness)
        GLES30.glUniform1f(loc(p, "uEmis"), mat.emissive)
        GLES30.glUniform1f(loc(p, "uAlpha"), mat.alpha)
        GLES30.glUniform1i(loc(p, "uUnlit"), if (mat.unlit) 1 else 0)
        m.bind()
        GLES30.glDrawElements(GLES30.GL_TRIANGLES, m.count, GLES30.GL_UNSIGNED_INT, 0)
    }
    private val tmp2 = FloatArray(16)

    private inline fun forEachVisible(n: GlNode, f: (GlNode) -> Unit) {
        val stack = ArrayList<GlNode>(); stack.add(n)
        while (stack.isNotEmpty()) {
            val c = stack.removeAt(stack.size - 1)
            if (!c.visible) continue
            f(c)
            for (i in c.children.indices.reversed()) stack.add(c.children[i])
        }
    }

    private fun setSrgb(l: Int, c: Int) = GLES30.glUniform3f(l, ((c shr 16) and 0xFF) / 255f, ((c shr 8) and 0xFF) / 255f, (c and 0xFF) / 255f)
    private fun setLinear(l: Int, c: Int) {
        fun lin(v: Int): Float { val f = v / 255f; return if (f <= 0.04045f) f / 12.92f else Math.pow(((f + 0.055f) / 1.055f).toDouble(), 2.4).toFloat() }
        GLES30.glUniform3f(l, lin((c shr 16) and 0xFF), lin((c shr 8) and 0xFF), lin(c and 0xFF))
    }

    private fun program(vs: String, fs: String): Int {
        fun shader(type: Int, src: String): Int {
            val s = GLES30.glCreateShader(type)
            GLES30.glShaderSource(s, src); GLES30.glCompileShader(s)
            val ok = IntArray(1); GLES30.glGetShaderiv(s, GLES30.GL_COMPILE_STATUS, ok, 0)
            if (ok[0] == 0) Log.e("NebGl", GLES30.glGetShaderInfoLog(s))
            return s
        }
        val p = GLES30.glCreateProgram()
        GLES30.glAttachShader(p, shader(GLES30.GL_VERTEX_SHADER, vs)); GLES30.glAttachShader(p, shader(GLES30.GL_FRAGMENT_SHADER, fs))
        GLES30.glLinkProgram(p)
        return p
    }
}
