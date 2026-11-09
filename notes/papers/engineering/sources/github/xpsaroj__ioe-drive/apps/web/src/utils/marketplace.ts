export const formatListingPrice = (price?: number | null): string =>
    price != null ? `Rs. ${price.toLocaleString()}` : "Contact for price";
