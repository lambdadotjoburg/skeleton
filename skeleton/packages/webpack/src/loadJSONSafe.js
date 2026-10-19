import fs from "fs";

export default function loadJSONSafe(fileURL) {
    try {
        if (!fs.existsSync(fileURL)) return null;
        return JSON.parse(
            fs.readFileSync(fileURL, "utf-8")
        );
    } catch(e) {
        console.warn(`[config] Failed to load JSON: ${fileURL}`);
        console.warn(e);
        return null;
    }
}