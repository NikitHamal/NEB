"use client"
import { use, useEffect, useState } from "react"
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ChevronLeft, Download, ExternalLink, FileWarning, PanelRightClose, PanelRightOpen, SearchX } from "lucide-react";

import { useResource, useFileDownloadUrl, useDownloadFile } from "@/hooks/queries/use-resources";
import { useMe, useMarkResourceAsRecentlyAccessed } from "@/hooks/queries/use-me";
import { useDocxPreviewHtml } from "@/hooks/queries/use-docx-preview";
import Button from "@/components/ui/Button";
import Loader from "@/components/ui/Loader";
import { PageStateHandler } from "@/components/layout";
import { getErrorMessage } from "@/lib/errors";
import { FILE_TYPE_META, DEFAULT_FILE_TYPE_META, getMimeKey, getHostname } from "@/components/common/resources";
import { UploaderInfo } from "@/components/common/user";

interface FilePreviewPageProps {
    params: Promise<{
        resourceId: string;
        fileId: string;
    }>
}

const DOCX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";

// Types the browser can render natively (PDF/images) or that we convert client-side (docx).
const INLINE_PREVIEWABLE_MIME_TYPES = new Set(["application/pdf", "image/jpeg", "image/png", DOCX_MIME_TYPE]);

const FilePreviewPage = ({
    params
}: FilePreviewPageProps) => {
    const { resourceId: rId, fileId: fId } = use(params);
    const resourceId = Number(rId);
    const fileId = Number(fId);

    const router = useRouter();

    const { data: resource, isPending, error } = useResource(resourceId);
    const activeFile = resource?.files.find((file) => file.id === fileId);

    const {
        data: downloadData,
        isPending: urlPending,
        isError: urlError,
        error: downloadError,
        refetch: refetchDownloadUrl,
    } = useFileDownloadUrl(resourceId, activeFile?.id);

    const { mutate: requestDownload, isPending: isPreparingDownload } = useDownloadFile(resourceId);

    const isDocx = activeFile?.mimeType === DOCX_MIME_TYPE;
    const {
        data: docxHtml,
        isPending: docxPending,
        isError: docxError,
    } = useDocxPreviewHtml(isDocx ? downloadData?.url : undefined);

    const { data: userData } = useMe();
    const { mutate: markAsRecentlyAccessed } = useMarkResourceAsRecentlyAccessed();

    const [hasRetriedImage, setHasRetriedImage] = useState(false);
    const [showSidebar, setShowSidebar] = useState(true);

    const isMissing = !resourceId || !fileId || isNaN(resourceId) || isNaN(fileId) || !resource || !activeFile;

    useEffect(() => {
        if (userData && resource) {
            markAsRecentlyAccessed(String(resource.id));
        }
        // Depend on userData.id, not the object, so an unrelated profile refetch doesn't re-fire this.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [userData?.id, resource?.id]);

    const handleDownload = () => {
        if (!activeFile) return;
        requestDownload(activeFile.id, {
            onSuccess: (url) => {
                // An <a> click (not location.href) so this doesn't act as a top-level
                // navigation - that would abort in-flight requests and the socket.io
                // connection before the browser even sees the attachment response.
                const link = document.createElement("a");
                link.href = url;
                link.rel = "noopener noreferrer";
                document.body.appendChild(link);
                link.click();
                link.remove();
            },
        });
    };

    const handleImageError = () => {
        // Signed URL may have expired (e.g. a tab left open a while) - retry once with a fresh one.
        if (!hasRetriedImage) {
            setHasRetriedImage(true);
            refetchDownloadUrl();
        }
    };

    const header = (
        <div className="flex items-center gap-2 mb-4 min-w-0">
            <Button
                icon={<ChevronLeft className="size-4" />}
                iconOnly
                variant="ghost"
                size="xs"
                className="border border-border shrink-0"
                onClick={() => router.back()}
                aria-label="Go back"
            />
            <h1 className="text-lg md:text-xl font-medium truncate">
                {activeFile?.originalFileName ?? "File Preview"}
            </h1>
        </div>
    )

    const emptyContent = (
        <div className="flex flex-col items-center justify-center gap-2 text-center">
            <SearchX className="size-8 text-foreground-tertiary" />
            <p className="text-foreground-secondary">This file could not be found.</p>
        </div>
    )

    if (isMissing || isPending) {
        return (
            <PageStateHandler
                isPending={isPending}
                error={error}
                isEmpty={!isPending && isMissing}
                header={header}
                loaderText="Loading file details. Please wait."
                emptyContent={emptyContent}
            >
                {null}
            </PageStateHandler>
        );
    }

    const canPreviewInline = INLINE_PREVIEWABLE_MIME_TYPES.has(activeFile.mimeType);

    const createdAt = new Date(resource.createdAt);
    const formattedCreatedAt = createdAt.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
    });

    return (
        <div className="min-h-screen bg-background text-foreground p-0 mx-auto">
            <div className="flex flex-col md:flex-row gap-6 items-start">
                {/* h-screen (not flex-1 alone) since flex-1's flex-basis:0 would collapse this pane's height when stacked in flex-col on mobile. */}
                <div className="order-2 w-full h-screen md:order-1 md:flex-1 flex items-center justify-center">
                    {urlPending ? (
                        <Loader text="Preparing preview..." />
                    ) : urlError || !downloadData ? (
                        <p className="text-error text-sm">
                            {getErrorMessage(downloadError, "Couldn't load this file's preview. Please try again.")}
                        </p>
                    ) : !canPreviewInline ? (
                        <div className="flex flex-col items-center gap-3 text-center py-10">
                            <FileWarning className="size-10 text-foreground-tertiary" />
                            <p className="text-sm text-foreground-secondary">
                                Preview isn&apos;t available for this file type. Download it to view it.
                            </p>
                        </div>
                    ) : activeFile.mimeType === "application/pdf" ? (
                        <iframe
                            src={downloadData.url}
                            title={activeFile.originalFileName}
                            className="w-full h-full"
                        />
                    ) : activeFile.mimeType === DOCX_MIME_TYPE ? (
                        <div className="w-full h-full overflow-auto bg-background p-6">
                            {docxPending ? (
                                <Loader text="Converting document..." />
                            ) : docxError || !docxHtml ? (
                                <p className="text-error text-sm">Couldn&apos;t render this document&apos;s preview.</p>
                            ) : (
                                // Sanitized via DOMPurify in useDocxPreviewHtml before it ever gets here.
                                <div className="docx-preview-content max-w-full" dangerouslySetInnerHTML={{ __html: docxHtml }} />
                            )}
                        </div>
                    ) : (
                        // Signed URLs are per-request and short-lived - plain <img>, not an oversight.
                        // eslint-disable-next-line @next/next/no-img-element
                        <img
                            src={downloadData.url}
                            alt={activeFile.originalFileName}
                            onError={handleImageError}
                            className="max-w-full max-h-full object-contain"
                        />
                    )}
                </div>

                {/* Unmounted entirely while collapsed, so the main pane's flex-1 takes the full row. */}
                {showSidebar && (
                    <div className="order-1 md:order-2 md:w-88 md:h-screen self-start overflow-y-auto p-4 md:px-0 md:pe-6">
                        <div className="w-full  shrink-0 flex flex-col gap-4 md:sticky overflow-y-auto">
                            <div className="flex items-center gap-2">
                                <Button
                                    icon={<ChevronLeft className="size-4" />}
                                    iconOnly
                                    variant="ghost"
                                    size="xs"
                                    className="border border-border shrink-0"
                                    onClick={() => router.back()}
                                    aria-label="Go back"
                                />
                                <div className="flex items-center gap-2 ms-auto">
                                    <Button
                                        icon={<Download className="size-4" />}
                                        iconOnly
                                        variant="primary"
                                        size="xs"
                                        onClick={handleDownload}
                                        disabled={isPreparingDownload}
                                        aria-label={isPreparingDownload ? "Preparing download..." : "Download file"}
                                    />
                                    {/* Desktop-only collapse toggle; `md:contents` avoids fighting Button's own `inline-flex` at the same breakpoint. */}
                                    <div className="hidden md:contents">
                                        <Button
                                            icon={<PanelRightClose className="size-4" />}
                                            iconOnly
                                            variant="ghost"
                                            size="xs"
                                            className="border border-border"
                                            onClick={() => setShowSidebar(false)}
                                            aria-label="Hide details"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="rounded-lg border border-border p-5">
                                <Link
                                    href={`/resources/r/${resource.id}`}
                                    className="text-lg font-semibold text-foreground hover:underline"
                                >
                                    {resource.title}
                                </Link>
                                <p className="mt-2 text-sm leading-relaxed text-foreground-secondary">
                                    {resource.description}
                                </p>

                                <div className="mt-4 border-t border-border pt-4">
                                    <UploaderInfo user={resource.uploader} subtitle={formattedCreatedAt} />
                                </div>

                                <Link
                                    href={`/offerings/${resource.subjectOffering.id}`}
                                    className="mt-4 flex items-center gap-1.5 border-t border-border pt-4 text-xs text-foreground-secondary hover:text-foreground hover:underline"
                                >
                                    <span className="font-medium text-foreground">{resource.subjectOffering.subject.code}</span>
                                    <span className="truncate">{resource.subjectOffering.subject.name}</span>
                                </Link>
                            </div>

                            <div className="rounded-lg border border-border p-5">
                                <p className="mb-3 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                    Attached files
                                </p>
                                <div className="flex flex-col gap-1.5">
                                    {resource.files.map((file) => {
                                        const { icon: Icon, className } = FILE_TYPE_META[getMimeKey(file.mimeType)] ?? DEFAULT_FILE_TYPE_META;

                                        return (
                                            <Link
                                                key={file.id}
                                                href={`/resources/r/${resource.id}/files/${file.id}`}
                                                className={`flex items-center gap-2 rounded-md border p-2 text-sm transition-colors ${file.id === activeFile.id
                                                    ? "border-accent bg-accent-soft"
                                                    : "border-border hover:bg-background-tertiary"
                                                    }`}
                                            >
                                                <span className={`flex size-7 shrink-0 items-center justify-center rounded-md ${className}`}>
                                                    <Icon className="size-3.5" />
                                                </span>
                                                <span className="truncate">{file.originalFileName}</span>
                                            </Link>
                                        );
                                    })}
                                </div>
                            </div>

                            {resource.links.length > 0 && (
                                <div className="rounded-lg border border-border p-5">
                                    <p className="mb-3 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                        Links
                                    </p>
                                    <div className="flex flex-col gap-1.5">
                                        {resource.links.map((link) => (
                                            <a
                                                key={link.id}
                                                href={link.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="flex items-center gap-2 rounded-md border border-border p-2 text-sm transition-colors hover:bg-background-tertiary"
                                            >
                                                <span className="flex size-7 shrink-0 items-center justify-center rounded-md bg-background-tertiary text-foreground-secondary">
                                                    <ExternalLink className="size-3.5" />
                                                </span>
                                                <span className="min-w-0">
                                                    <span className="block truncate">{link.label}</span>
                                                    <span className="block truncate font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                                                        {getHostname(link.url)}
                                                    </span>
                                                </span>
                                            </a>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>

            {/* Overlays the full-width main pane rather than taking up flex layout space. */}
            {!showSidebar && (
                <Button
                    variant="ghost"
                    size="sm"
                    className="absolute top-3 right-4 p-0 md:flex items-center justify-center backdrop-blur-sm border"
                    icon={<PanelRightOpen className="size-5" />}
                    iconOnly
                    onClick={() => setShowSidebar(true)}
                    aria-label="Show details"
                />
            )}
        </div>
    )
}

export default FilePreviewPage;
