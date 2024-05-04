<script>
	import { module } from '$lib/store.js';

	import SVG from '$lib/svg.svelte';
	import Marked from '$lib/marked.svelte';
	import Button from '$lib/button/button.svelte';
</script>

<div
	class="title"
	class:good={$module.status == 200}
	class:bad={$module.status == 400}
	class:caution={$module.status == 201}
>
	{#if $module.status == 200}
		<SVG type="check" size="20" />
	{:else if $module.status == 400}
		<SVG type="close" />
	{:else if $module.status == 201}
		<SVG type="info" size="20" />
	{/if}
	{$module?.title || 'no title'}
</div>
<div class="body">
	<Marked md={$module?.message || 'no message'} />
	{#if $module.button}
		<br />
		{#each $module.button as b}
			<Button on:click={b.fn}>
				<SVG type={b.icon} />
				{b.name}
			</Button>
		{/each}
	{/if}
</div>

<style>
	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: var(--sp2);
		color: var(--ac6_);
		fill: var(--ac6_);
	}

	.body {
		background-color: var(--ac6);
		color: var(--ac2);
		padding: var(--sp3);
	}

	.good {
		background-color: var(--cl5);
	}
	.bad {
		background-color: var(--cl4);
	}
	.caution {
		background-color: var(--cl6);
	}
</style>
