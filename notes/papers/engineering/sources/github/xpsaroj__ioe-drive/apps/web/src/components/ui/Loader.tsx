export default function Loader({text}: {text?: string}) {
    return (
        <div className="flex flex-col items-center justify-center w-full py-20">
            <div className="animate-spin h-8 w-8 border-4 border-foreground-secondary border-t-foreground rounded-full" />
            {text && <p className="mt-2 text-foreground-secondary">{text}</p>}
        </div>
    );
}

export { Loader };