import {createSearchParamsCache, parseAsString} from "nuqs/server";


export const fileParsers = {
    filename: parseAsString.withDefault(""),
}

export const fileParamsCache = createSearchParamsCache(fileParsers);