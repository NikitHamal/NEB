"use client";
import { ChevronRight, Compass } from "lucide-react";

import ResourcePreviewTile from "./ResourcePreviewTile";
import Button from "@/components/ui/Button";
import { useRecentResources } from "@/hooks/queries/use-me";
import { getRelativeTime } from "@/utils/time";

// Shown as a single row of 2, so only that many are ever fetched/rendered.
const RECENT_RESOURCES_SHOWN = 2;

interface JumpBackInProps {
  /** Stretches to match a taller grid sibling (Dashboard); leave off when stacked (library hub). */
  fillHeight?: boolean;
}

// Shared between the dashboard and the library hub.
const JumpBackIn = ({ fillHeight = false }: JumpBackInProps) => {
  const { data, isPending } = useRecentResources(1);
  const items = data?.items.slice(0, RECENT_RESOURCES_SHOWN);

  return (
    <div className={fillHeight ? "h-full flex flex-col" : ""}>
      <div className="flex items-center justify-between gap-4 mb-6">
        <h2 className="text-lg font-semibold text-foreground">Jump Back In</h2>
        <Button
          href="/library/recent"
          variant="ghost"
          size="xs"
          icon={<ChevronRight className="size-3.5" />}
          iconPosition="right"
          className="text-foreground-secondary hover:text-foreground shrink-0"
        >
          View history
        </Button>
      </div>

      {isPending ? (
        <div className={`grid grid-cols-1 sm:grid-cols-2 gap-4 ${fillHeight ? "flex-1" : ""}`}>
          {Array.from({ length: RECENT_RESOURCES_SHOWN }).map((_, i) => (
            <div key={i} className="h-full min-h-36 rounded-lg bg-skeleton-base animate-pulse" />
          ))}
        </div>
      ) : items && items.length > 0 ? (
        <div className={`grid grid-cols-1 sm:grid-cols-2 gap-4 ${fillHeight ? "flex-1" : ""}`}>
          {items.map((item) => (
            <ResourcePreviewTile
              key={item.resourceId}
              resourceId={item.resourceId}
              title={item.resource.title}
              subjectCode={item.resource.subjectOffering?.subject?.code}
              type={item.resource.type}
              timeLabel={`Viewed ${getRelativeTime(item.accessedAt)}`}
              uploader={item.resource.uploader}
            />
          ))}
        </div>
      ) : (
        <div className={`flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border py-10 px-4 text-center ${fillHeight ? "flex-1" : ""}`}>
          <span className="flex size-10 items-center justify-center rounded-full bg-accent-soft text-accent">
            <Compass className="size-5" />
          </span>
          <div>
            <p className="text-sm font-medium text-foreground">Nothing viewed yet</p>
            <p className="text-sm text-foreground-secondary mt-1">
              Browse resources for your semester and they&apos;ll show up here.
            </p>
          </div>
          <Button href="/resources" size="sm" variant="secondary" className="mt-1">
            Browse resources
          </Button>
        </div>
      )}
    </div>
  );
};

export default JumpBackIn;
