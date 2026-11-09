import { useQuery } from "@tanstack/react-query";

// mammoth/dompurify are dynamically imported so their weight only loads for an actual
// .docx preview, not every visit to the file preview page (PDF/image previews never need them).
export function useDocxPreviewHtml(url?: string) {
    return useQuery({
        queryKey: ["docx-preview", url],
        queryFn: async () => {
            const [{ default: mammoth }, { default: DOMPurify }] = await Promise.all([
                import("mammoth"),
                import("dompurify"),
            ]);

            const response = await fetch(url!);
            if (!response.ok) {
                throw new Error("Failed to fetch file");
            }

            const arrayBuffer = await response.arrayBuffer();
            const { value } = await mammoth.convertToHtml({ arrayBuffer });

            return DOMPurify.sanitize(value);
        },
        enabled: !!url,
    });
}
