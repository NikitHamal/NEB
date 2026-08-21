package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.AvatarStyleResponse
import com.neb.ians.data.api.AvatarStyleUpdateRequest
import com.neb.ians.data.api.AvatarStyleUpdateResponse
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AvatarRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    data class AvatarStyle(
        val avatarUrl: String,
        val usePp: Boolean,
        val hue: Int,
        val tone: Double,
        val bg: String,
        val anim: String,
        val shape: String,
        val expression: String,
        val color: String,
        val bgcolor: String,
        val eyecolor: String
    )

    suspend fun getStyle(): Result<AvatarStyle> = runCatching {
        val bearer = authRepository.getBearerToken() ?: throw IllegalStateException("Not signed in")
        val res = apiService.getAvatarStyle(bearer)
        AvatarStyle(
            avatarUrl = res.avatarUrl.ifBlank { res.avatarUrlCamel.orEmpty() },
            usePp = res.avatarUsePp,
            hue = res.raw.hue,
            tone = res.raw.tone,
            bg = res.raw.bg,
            anim = res.raw.anim,
            shape = res.raw.shape,
            expression = res.raw.expression,
            color = res.raw.color,
            bgcolor = res.raw.bgcolor,
            eyecolor = res.raw.eyecolor
        )
    }

    suspend fun updateStyle(request: AvatarStyleUpdateRequest): Result<AvatarStyleUpdateResponse> = runCatching {
        val bearer = authRepository.getBearerToken() ?: throw IllegalStateException("Not signed in")
        apiService.updateAvatarStyle(bearer, request)
    }
}
