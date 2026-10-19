import { spawn } from "node:child_process";

export async function exec(
    command: string,
    args: string[],
    cwd?: string,
): Promise<void> {

    await new Promise<void>(
        (resolve, reject) => {

            const child = spawn(
                command,
                args,
                {
                    cwd: cwd,
                    stdio: "inherit",
                    shell: true,
                }
            );

            child.on("error", reject);

            child.on(
                "exit", (code) => {

                    if (code === 0) {
                        resolve();
                        return;
                    }

                    reject(
                        new Error(
                            `${command} exited with code ${code}`
                        )
                    );
                }
            );
        }
    );
}