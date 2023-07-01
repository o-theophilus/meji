<script>
	import { goto } from '$app/navigation';
	import { module } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import SVG from '$lib/comp/svg.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Button from '$lib/comp/button.svelte';

	export let data;
	let title = data?.title ? data.title : 'no title';
	let message = data?.message ? data.message : 'no message';
	let status = data?.status;
</script>

<Card>
	<div
		class="title"
		class:good={status == 'good'}
		class:bad={status == 'bad'}
		class:caution={status == 'warning'}
	>
		{#if status == 'good'}
			<SVG type="check" size="20" />
		{:else if status == 'bad'}
			<SVG type="close" />
		{:else if status == 'warning'}
			<SVG type="info" size="20" />
		{/if}
		{title}
	</div>
	<div class="body">
		<Body>
			<Marked md={message} />
			{#each data?.button as button}
				<Button
					name={button.name}
					icon={button.icon}
					on:click={() => {
						if (button.href) {
							goto(button.href);
						} else {
							$module = '';
						}
					}}
				/>
			{/each}
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
