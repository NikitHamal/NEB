"use client"
import { Suspense, useState } from "react";
import { Plus } from "lucide-react";

import { ItemList } from "@/components/common/list";
import { MarketplaceListingCard } from "@/components/common/marketplace";
import Select from "@/components/ui/Select";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";
import { useListings } from "@/hooks/queries/use-marketplace";
import { getErrorMessage } from "@/lib/errors";
import { usePageParam } from "@/hooks/use-page-param";
import { useDebouncedValue } from "@/hooks/use-debounced-value";
import {
    MarketplaceListingType,
    MarketplaceListingTypeLabel,
    MarketplaceCategory,
    MarketplaceCategoryLabel,
} from "@/types/entities";

const MarketBrowseContent = () => {
    const { page, setPage } = usePageParam();

    const [type, setType] = useState<MarketplaceListingType | "">("");
    const [category, setCategory] = useState<MarketplaceCategory | "">("");
    const [query, setQuery] = useState("");
    const debouncedQuery = useDebouncedValue(query.trim());

    const filters = {
        type: type || undefined,
        category: category || undefined,
        q: debouncedQuery || undefined,
    };

    const { data, isPending, error, isPlaceholderData } = useListings(filters, page);
    const listings = data?.items ?? [];

    return (
        <div className="min-h-screen flex flex-col bg-background text-foreground max-w-7xl mx-auto md:p-8 p-6 space-y-6">
            <div className="flex flex-wrap items-start justify-between gap-4 pb-6 border-b border-border">
                <div>
                    <h1 className="text-2xl md:text-3xl font-bold text-foreground">Market</h1>
                    <p className="text-foreground-secondary mt-2 max-w-2xl">
                        Buy, sell, or trade textbooks, calculators, and drafting tools with fellow IOE students.
                    </p>
                </div>
                <Button href="/market/create" icon={<Plus className="size-4" />} className="shrink-0">
                    Post a Listing
                </Button>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
                <div className="sm:col-span-2">
                    <Input
                        placeholder="Search listings..."
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value);
                            setPage(1);
                        }}
                    />
                </div>
                <Select
                    value={type}
                    onChange={(e) => {
                        setType(e.target.value as MarketplaceListingType | "");
                        setPage(1);
                    }}
                    options={[
                        { value: "", label: "All Types" },
                        ...Object.values(MarketplaceListingType).map((t) => ({
                            value: t,
                            label: MarketplaceListingTypeLabel[t],
                        })),
                    ]}
                />
                <Select
                    value={category}
                    onChange={(e) => {
                        setCategory(e.target.value as MarketplaceCategory | "");
                        setPage(1);
                    }}
                    options={[
                        { value: "", label: "All Categories" },
                        ...Object.values(MarketplaceCategory).map((c) => ({
                            value: c,
                            label: MarketplaceCategoryLabel[c],
                        })),
                    ]}
                />
            </div>

            <div className="space-y-6">
                <ItemList
                    items={listings}
                    loading={isPending}
                    error={error ? getErrorMessage(error, "Couldn't load listings. Please try again.") : null}
                    renderItem={(listing) => <MarketplaceListingCard listing={listing} />}
                    emptyMessage="No listings found."
                />
                <Pagination
                    page={page}
                    totalPages={data?.meta?.totalPages ?? 1}
                    onPageChange={setPage}
                    disabled={isPlaceholderData}
                />
            </div>
        </div>
    );
};

const MarketPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading market listings. Please wait." />
            </div>
        }>
            <MarketBrowseContent />
        </Suspense>
    );
};

export default MarketPage;
