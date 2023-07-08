<script>
	import { module } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import SVG from '$lib/comp/svg.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Button from '$lib/comp/button.svelte';
</script>

<Card>
	<div
		class="title"
		class:good={$module.status == 200}
		class:bad={$module.status == 401}
		class:caution={$module.status == 201}
	>
		{#if $module.status == 200}
			<SVG type="check" size="20" />
		{:else if $module.status == 401}
			<SVG type="close" />
		{:else if $module.status == 201}
			<SVG type="info" size="20" />
		{/if}
		{$module?.title || 'no title'}
	</div>
	<div class="body">
		<Body>
			<Marked md={$module?.message || 'no message'} />
			{#if $module.button}
				{#each $module.button as b}
					<Button name={b.name} icon={b.icon} on:click={b.fn} />
				{/each}
			{/if}
		</Body>
	</div>
</Card>

<style>
	.title {
		display: flex;
		align-items: center;
		gap: var(--gap2);

		padding: var(--gap2);
		color: var(--light_color);
		fill: var(--light_color);
	}

	.body {
		background: var(--foreground);
	}

	.good {
		background-color: var(--color5);
	}
	.bad {
		background-color: var(--color4);
	}
	.caution {
		background-color: var(--color6);
	}
</style>
