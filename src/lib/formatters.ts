import { NEREntities } from '@/types/candidate';

/**
 * Format a string array field - returns first element or "NA"
 * @param arr Array of strings (optional)
 * @returns First element or "NA" if empty/undefined
 */
export function formatField(arr: string[] | undefined): string {
    return arr && arr.length > 0 ? arr[0] : 'NA';
}

/**
 * Format a string array for display - returns joined string or "NA"
 * @param arr Array of strings (optional)
 * @param separator Separator for joining (default: ", ")
 * @returns Joined string or "NA" if empty/undefined
 */
export function formatArrayField(arr: string[] | undefined, separator: string = ', '): string {
    return arr && arr.length > 0 ? arr.join(separator) : 'NA';
}

/**
 * Format NER entities with NA handling
 * @param entities NER entities object
 * @returns Formatted entities with NA for empty fields
 */
export function formatNEREntities(entities: NEREntities): {
    PERSON: string;
    ORG: string;
    GPE: string;
    DATE: string;
} {
    return {
        PERSON: formatArrayField(entities.PERSON),
        ORG: formatArrayField(entities.ORG),
        GPE: formatArrayField(entities.GPE),
        DATE: formatArrayField(entities.DATE),
    };
}
