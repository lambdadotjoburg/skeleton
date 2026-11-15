<script lang="ts">
    let message: string = "Skeleton + FastAPI + Svelte 5 + Webpack";
</script>

<svelte:head>
    <title>Skeleton + Svelte</title>
</svelte:head>

<main>
    <h1>{message}</h1>
</main>

<style>
    main {
        padding: 2rem;
        font-family: Arial, sans-serif;
    }

    h1 {
        color: #ff3e00;
    }
</style>