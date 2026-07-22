package com.neb.ians.ui.screens.auth

import android.view.View
import android.webkit.WebView
import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import com.neb.ians.data.repository.AuthState
import com.neb.ians.data.repository.AuthRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first

@Composable
fun SplashScreen(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit
) {
    val scale = remember { Animatable(0.6f) }
    val isDark = isSystemInDarkTheme()
    
    LaunchedEffect(key1 = true) {
        scale.animateTo(
            targetValue = 1.0f,
            animationSpec = keyframes {
                durationMillis = 800
                0.6f at 0 with FastOutSlowInEasing
                1.05f at 600 with FastOutSlowInEasing
                1.0f at 800 with FastOutSlowInEasing
            }
        )
        
        delay(2600)
        
        when (val state = authRepository.authState.first()) {
            is AuthState.Guest -> onNavigateToHome()
            is AuthState.Authenticated -> {
                if (state.isProfileComplete) {
                    onNavigateToHome()
                } else {
                    onNavigateToCompleteProfile()
                }
            }
            else -> onNavigateToLogin()
        }
    }
    
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.surface
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding(),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
                modifier = Modifier.fillMaxSize()
            ) {
                // Top App Logo Icon
                Surface(
                    modifier = Modifier
                        .size(80.dp)
                        .scale(scale.value),
                    shape = MaterialTheme.shapes.extraLarge,
                    color = MaterialTheme.colorScheme.primaryContainer,
                    tonalElevation = 4.dp
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Image(
                            painter = painterResource(id = com.neb.ians.R.drawable.ic_nebians_logo),
                            contentDescription = "NEBians Logo",
                            modifier = Modifier.size(52.dp),
                            contentScale = ContentScale.Fit
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Smooth Handwritten SVG Text Animation
                NebiansSvgAnimation(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp),
                    isDarkTheme = isDark
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = "Nepali Learning Community",
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    letterSpacing = 0.5.sp,
                    modifier = Modifier.scale(scale.value)
                )
            }
        }
    }
}

@Composable
private fun NebiansSvgAnimation(
    modifier: Modifier = Modifier,
    isDarkTheme: Boolean = false
) {
    val svgHtml = remember(isDarkTheme) {
        val stop0 = if (isDarkTheme) "#60A5FA" else "#A7C2F8"
        val stop1 = if (isDarkTheme) "#3B82F6" else "#2563EB"
        val stop2 = if (isDarkTheme) "#93C5FD" else "#07255E"
        val haloBg = "transparent"
        
        """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap');
          html, body {
            margin: 0; padding: 0;
            width: 100%; height: 100%;
            background: transparent;
            display: flex; align-items: center; justify-content: center;
            overflow: hidden;
          }
          svg { width: 100%; height: 100%; }
          .screen { animation: screenIn .5s ease both; }
          @keyframes screenIn { from { opacity: 0; } to { opacity: 1; } }
          .brand-word {
            font-family: 'Dancing Script', 'Segoe Script', 'Brush Script MT', cursive;
            font-weight: 700;
            font-size: 88px;
            fill: url(#brand);
          }
        </style>
        </head>
        <body>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 432 300" preserveAspectRatio="xMidYMid meet">
          <defs>
            <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0"   stop-color="$stop0"/>
              <stop offset="0.5" stop-color="$stop1"/>
              <stop offset="1"   stop-color="$stop2"/>
            </linearGradient>
            <radialGradient id="halo" gradientUnits="userSpaceOnUse" cx="216" cy="150" r="220">
              <stop offset="0"    stop-color="#ffffff" stop-opacity="${if (isDarkTheme) "0.08" else "0.85"}"/>
              <stop offset="0.55" stop-color="#ffffff" stop-opacity="${if (isDarkTheme) "0.02" else "0.20"}"/>
              <stop offset="1"    stop-color="#ffffff" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0"     stop-color="#fff"/>
              <stop offset="0.939" stop-color="#fff"/>
              <stop offset="1"     stop-color="#000"/>
            </linearGradient>
            <mask id="reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="432" height="300">
              <rect x="-460" y="0" width="460" height="300" fill="url(#edge)">
                <animate attributeName="x"
                         values="-460;0;0;-460;-460"
                         keyTimes="0;0.435;0.696;0.913;1"
                         keySplines="0.4 0 0.2 1; 0 0 1 1; 0.4 0 0.2 1; 0 0 1 1"
                         calcMode="spline"
                         dur="4.6s" repeatCount="indefinite"/>
              </rect>
            </mask>
          </defs>
          <g class="screen">
            <rect width="432" height="300" fill="$haloBg"/>
            <rect width="432" height="300" fill="url(#halo)"/>
            <g mask="url(#reveal)">
              <text class="brand-word" x="216" y="175" text-anchor="middle">Nebians</text>
            </g>
          </g>
        </svg>
        </body>
        </html>
        """.trimIndent()
    }

    AndroidView(
        factory = { context ->
            WebView(context).apply {
                setBackgroundColor(android.graphics.Color.TRANSPARENT)
                setLayerType(View.LAYER_TYPE_HARDWARE, null)
                settings.javaScriptEnabled = true
                settings.loadWithOverviewMode = true
                settings.useWideViewPort = true
                settings.domStorageEnabled = true
                isVerticalScrollBarEnabled = false
                isHorizontalScrollBarEnabled = false
                loadDataWithBaseURL("https://fonts.googleapis.com", svgHtml, "text/html", "UTF-8", null)
            }
        },
        modifier = modifier
    )
}