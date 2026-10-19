import path from "node:path";
import fs from "node:fs/promises";

export async function clean(
    root: string
): Promise<void> {

    await cleanBuildInfo(root);
    await cleanDist(root);
}

async function cleanBuildInfo(
    root: string
): Promise<void> {

    await removeBuildInfo(
        root
    );

    await removeBuildInfoTree(
        path.join(root, "app")
    );

    await removeBuildInfoTree(
        path.join(root, "packages")
    );
}

async function removeBuildInfo(
    directory: string
): Promise<void> {

    const entries = await fs.readdir(
        directory,
        { withFileTypes: true }
    );

    for (const entry of entries) {

        if (
            entry.isFile() &&
            entry.name.endsWith(".tsbuildinfo")
        ) {
            await fs.rm(
                path.join(directory, entry.name),
                { force: true }
            );
        }
    }
}

async function removeBuildInfoTree(
    directory: string
): Promise<void> {

    try {

        const entries = await fs.readdir(
            directory,
            { withFileTypes: true }
        );

        for (const entry of entries) {

            const target = path.join(
                directory,
                entry.name
            );

            if (entry.isDirectory()) {

                await removeBuildInfoTree(
                    target
                );

                continue;
            }

            if (
                entry.isFile() &&
                entry.name.endsWith(".tsbuildinfo")
            ) {
                await fs.rm(
                    target,
                    { force: true }
                );
            }
        }

    } catch (error: any) {

        if (error.code === "ENOENT") {
            return;
        }

        throw error;
    }
}

async function cleanDist(
    root: string
): Promise<void> {

    await removeDist(
        path.join(root, "dist")
    );

    await removeDistTree(
        path.join(root, "app")
    );

    await removeDistTree(
        path.join(root, "packages")
    );
}

async function removeDist(
    directory: string
): Promise<void> {

    await fs.rm(
        directory,
        {
            recursive: true,
            force: true,
        }
    );
}

async function removeDistTree(
    directory: string
): Promise<void> {

    try {

        const entries = await fs.readdir(
            directory,
            { withFileTypes: true }
        );

        for (const entry of entries) {

            const target = path.join(
                directory,
                entry.name
            );

            if (
                entry.isDirectory() &&
                entry.name === "dist"
            ) {
                await fs.rm(
                    target,
                    {
                        recursive: true,
                        force: true,
                    }
                );

                continue;
            }

            if (entry.isDirectory()) {

                await removeDistTree(
                    target
                );
            }
        }

    } catch (error: any) {

        if (error.code === "ENOENT") {
            return;
        }

        throw error;
    }
}