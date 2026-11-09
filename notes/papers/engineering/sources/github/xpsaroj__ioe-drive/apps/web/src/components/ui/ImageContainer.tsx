import Image from "next/image";
import Link from "next/link";

interface ImageContainerProps {
    src: string;
    alt: string;
    width: number;
    height: number;
    href?: string;
}

export default function ImageContainer({ src, alt, width, height, href }: ImageContainerProps) {

    const InnerImage = (
        <Image
            src={src}
            alt={alt}
            fill
            className="object-cover rounded-lg h-full w-full"
        />
    );

    return (
        <div
            className={`image-container relative rounded-lg overflow-hidden justify-center items-center`}
            style={{ width: `${width}rem`, height: `${height}rem` }}
        >
            {href ? (
                <Link href={href}>
                    {InnerImage}
                </Link>
            ) : (
                <>
                    {InnerImage}
                </>
            )}
        </div>
    );
}