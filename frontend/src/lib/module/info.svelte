<script>
	import { module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import SVG from '$lib/comp/svg.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Button from '$lib/button.svelte';
</script>

<Card>
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
		gap: var(--sp2);

		padding: var(--sp2);
		color: var(--light_color);
		fill: var(--light_color);
	}

	.body {
		background: var(--ac4);
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
