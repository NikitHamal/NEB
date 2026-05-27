package com.neb.ians.navigation

object Routes {
    const val HOME = "home"
    const val RESOURCES = "resources"
    const val FORUM = "forum"
    const val PROFILE = "profile"
    const val SEARCH = "search"
    const val PDF_VIEWER = "pdf_viewer/{resourceId}"
    const val FORUM_POST = "forum_post/{postId}"
    const val CREATE_POST = "create_post"
    const val REPLY = "reply/{postId}/{replyToId}"

    fun pdfViewer(resourceId: Long) = "pdf_viewer/$resourceId"
    fun forumPost(postId: Long) = "forum_post/$postId"
    fun reply(postId: Long, replyToId: Long = -1) = "reply/$postId/$replyToId"
}
