import path from "node:path";
import fs from "node:fs/promises";

import { clean } from "./clean.js";

export async function purge(
    root: string
): Promise<void> {

    root = path.resolve(root);

    // ---------------------------------------------------------
    // Clean generated build output
    // ---------------------------------------------------------

    await clean(root);

    // ---------------------------------------------------------
    // Remove nested build artifacts
    // ---------------------------------------------------------

    await removeBuildArtifacts(root);

    // ---------------------------------------------------------
    // Remove package lock files
    // ---------------------------------------------------------

    await removePackageLocks(root);

    // ---------------------------------------------------------
    // Remove all installed Node.js dependencies
    // ---------------------------------------------------------

    await removeNodeModulesTree(root);

    // ---------------------------------------------------------
    // Remove Python type-checking caches
    // ---------------------------------------------------------

    await removeDirectoryTree(root, ".mypy_cache");

    // ---------------------------------------------------------
    // Remove generated Skeleton package tarballs
    // ---------------------------------------------------------

    // ---------------------------------------------------------
    // Remove generated Skeleton artifacts
    // ---------------------------------------------------------

    await fs.rm(
        path.join(root, ".skeleton"),
        {
            recursive: true,
            force: true,
        }
    );

    await fs.rm(
        path.join(
            root,
            "skeleton",
            "packages",
            ".skeleton"
        ),
        {
            recursive: true,
            force: true,
        }
    );
}

async function removePackageLocks(
    directory: string
): Promise<void> {

    let entries;

    try {

        entries = await fs.readdir(
            directory,
            { withFileTypes: true }
        );

    } catch (error: any) {

        if (error.code === "ENOENT") {
            return;
        }

        throw error;
    }

    for (const entry of entries) {

        const target = path.join(
            directory,
            entry.name
        );

        if (
            entry.isFile() &&
            entry.name === "package-lock.json"
        ) {

            await fs.rm(
                target,
                { force: true }
            );

            continue;
        }

        if (entry.isDirectory()) {

            // Do not traverse dependency trees that will be removed.
            if (entry.name === "node_modules") {
                continue;
            }

            await removePackageLocks(target);
        }
    }
}

async function removeDirectoryTree(
    directory: string,
    name: string
): Promise<void> {

    let entries;

    try {

        entries = await fs.readdir(
            directory,
            { withFileTypes: true }
        );

    } catch (error: any) {

        if (error.code === "ENOENT") {
            return;
        }

        throw error;
    }

    for (const entry of entries) {

        if (!entry.isDirectory()) {
            continue;
        }

        const target = path.join(
            directory,
            entry.name
        );

        if (entry.name === name) {

            await fs.rm(
                target,
                {
                    recursive: true,
                    force: true,
                }
            );

            continue;
        }

        await removeDirectoryTree(
            target,
            name
        );
    }
}

async function removeNodeModulesTree(
    directory: string
): Promise<void> {

    let entries;

    try {

        entries = await fs.readdir(
            directory,
            { withFileTypes: true }
        );

    } catch (error: any) {

        if (error.code === "ENOENT") {
            return;
        }

        throw error;
    }

    for (const entry of entries) {

        if (!entry.isDirectory()) {
            continue;
        }

        const target = path.join(
            directory,
            entry.name
        );

        if (entry.name === "node_modules") {

            await fs.rm(
                target,
                {
                    recursive: true,
                    force: true,
                }
            );

            continue;
        }

        await removeNodeModulesTree(target);
    }
}

async function removeBuildArtifacts(
    directory: string
): Promise<void> {

    let entries;

    try {

        entries = await fs.readdir(
            directory,
            { withFileTypes: true }
        );

    } catch (error: any) {

        if (error.code === "ENOENT") {
            return;
        }

        throw error;
    }

    for (const entry of entries) {

        if (!entry.isDirectory()) {

            if (
                entry.isFile() &&
                entry.name === "tsconfig.tsbuildinfo"
            ) {
                await fs.rm(
                    path.join(directory, entry.name),
                    { force: true }
                );
            }

            continue;
        }

        const target = path.join(
            directory,
            entry.name
        );

        if (entry.name === "dist") {

            await fs.rm(
                target,
                {
                    recursive: true,
                    force: true,
                }
            );

            continue;
        }

        // These directories are already handled elsewhere.
        if (
            entry.name === "node_modules" ||
            entry.name === ".skeleton"
        ) {
            continue;
        }

        await removeBuildArtifacts(target);
    }
}