import { features } from "@/constants/home";
import FeatureList from "@/components/ui/FeatureList";

export default function Features() {
    return (
        <section className="bg-background py-20">
            <div className="container mx-auto px-6">
                <h2 className="text-3xl text-foreground font-bold mb-8 text-center">
                    What this site offers?
                </h2>
            </div>

            <div className="container max-w-4xl mx-auto px-6">
                <FeatureList items={features} />
            </div>
        </section>
    );
}
