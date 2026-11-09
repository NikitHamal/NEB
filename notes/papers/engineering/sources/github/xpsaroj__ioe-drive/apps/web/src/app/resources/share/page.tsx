import { ResourceUploadForm } from "@/components/common/resources";

const ResourceSharePage = () => {
    return (
        <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto space-y-6 md:space-y-8">
            <div>
                <h1 className="text-2xl md:text-3xl font-bold">Share Resources</h1>
                <p className="text-foreground-secondary mt-2">Upload notes, books, and past questions to help your peers succeed.</p>
            </div>
            <ResourceUploadForm />
        </div>
    );
};

export default ResourceSharePage;
