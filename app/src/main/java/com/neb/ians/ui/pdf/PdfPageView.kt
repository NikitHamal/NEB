package com.neb.ians.ui.pdf

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import com.neb.ians.data.model.AnnotationType
import com.neb.ians.data.model.PdfAnnotation
import kotlin.math.max
import kotlin.math.min

class PdfPageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private var pageBitmap: Bitmap? = null
    private var annotations: List<PdfAnnotation> = emptyList()
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val highlightPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#66FFEB3B")
        style = Paint.Style.FILL
    }
    private val underlinePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#FF2196F3")
        strokeWidth = 6f
        style = Paint.Style.STROKE
    }
    private val notePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#FFFF9800")
        style = Paint.Style.FILL
    }
    private val textPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.BLACK
        textSize = 28f
    }

    private var scaleX = 1f
    private var scaleY = 1f

    private var onAreaSelectedListener: ((Float, Float, Float, Float) -> Unit)? = null
    private var selectionStartX = 0f
    private var selectionStartY = 0f
    private var selectionEndX = 0f
    private var selectionEndY = 0f
    private var isSelecting = false

    fun setPageBitmap(bitmap: Bitmap?) {
        pageBitmap = bitmap
        invalidate()
    }

    fun setAnnotations(list: List<PdfAnnotation>) {
        annotations = list
        invalidate()
    }

    fun setOnAreaSelectedListener(listener: (x: Float, y: Float, width: Float, height: Float) -> Unit) {
        onAreaSelectedListener = listener
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val bmp = pageBitmap ?: return

        scaleX = width.toFloat() / bmp.width.toFloat()
        scaleY = height.toFloat() / bmp.height.toFloat()
        val matrix = android.graphics.Matrix()
        matrix.setScale(scaleX, scaleY)
        canvas.drawBitmap(bmp, matrix, paint)

        for (annotation in annotations) {
            val rect = RectF(
                annotation.x * scaleX,
                annotation.y * scaleY,
                (annotation.x + annotation.width) * scaleX,
                (annotation.y + annotation.height) * scaleY
            )
            when (annotation.type) {
                AnnotationType.HIGHLIGHT -> {
                    canvas.drawRect(rect, highlightPaint)
                }
                AnnotationType.UNDERLINE -> {
                    canvas.drawLine(rect.left, rect.bottom, rect.right, rect.bottom, underlinePaint)
                }
                AnnotationType.STICKY_NOTE -> {
                    canvas.drawCircle(rect.centerX(), rect.centerY(), 24f, notePaint)
                    annotation.noteText?.let {
                        canvas.drawText(it, rect.centerX() + 30f, rect.centerY(), textPaint)
                    }
                }
            }
        }

        if (isSelecting) {
            val selRect = RectF(
                min(selectionStartX, selectionEndX),
                min(selectionStartY, selectionEndY),
                max(selectionStartX, selectionEndX),
                max(selectionStartY, selectionEndY)
            )
            paint.color = Color.parseColor("#4400E676")
            paint.style = Paint.Style.FILL
            canvas.drawRect(selRect, paint)
            paint.color = Color.parseColor("#FF00E676")
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 2f
            canvas.drawRect(selRect, paint)
        }
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                isSelecting = true
                selectionStartX = event.x
                selectionStartY = event.y
                selectionEndX = event.x
                selectionEndY = event.y
                invalidate()
            }
            MotionEvent.ACTION_MOVE -> {
                selectionEndX = event.x
                selectionEndY = event.y
                invalidate()
            }
            MotionEvent.ACTION_UP -> {
                isSelecting = false
                invalidate()
                val x = min(selectionStartX, selectionEndX) / scaleX
                val y = min(selectionStartY, selectionEndY) / scaleY
                val w = max(selectionStartX, selectionEndX) / scaleX - x
                val h = max(selectionStartY, selectionEndY) / scaleY - y
                if (w > 20 && h > 10) {
                    onAreaSelectedListener?.invoke(x, y, w, h)
                }
            }
        }
        return true
    }
}
