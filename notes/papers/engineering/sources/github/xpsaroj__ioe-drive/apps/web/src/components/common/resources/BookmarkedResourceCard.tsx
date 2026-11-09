import type { BookmarkedResourceItem } from "@/types/api";
import { getRelativeTime } from "@/utils/time";
import ResourceCard from "./ResourceCard";

interface Props {
    item: BookmarkedResourceItem;
}

const BookmarkedResourceCard = ({ item }: Props) => {
    const { bookmarkedAt, resource } = item;

    return (
        <ResourceCard
            resource={resource}
            meta={`Saved ${getRelativeTime(bookmarkedAt)}`}
        />
    );
};

export default BookmarkedResourceCard;
