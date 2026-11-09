import type { RecentResourceItem } from "@/types/api";
import { getRelativeTime } from "@/utils/time";
import ResourceCard from "./ResourceCard";

interface Props {
    item: RecentResourceItem;
}

const RecentResourceCard = ({ item }: Props) => {
    const { accessedAt, resource } = item;

    return (
        <ResourceCard
            resource={resource}
            meta={`Viewed ${getRelativeTime(accessedAt)}`}
        />
    );
};

export default RecentResourceCard;
