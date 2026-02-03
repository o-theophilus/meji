<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Card } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import Item from '../shop/item.svelte';

	let width = $state();
	let open = $state(true);
	let { items = [], _title, id = '' } = $props();

	onMount(async () => {
		if (!app.tags) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.tags = resp.tags;
			}
		}
	});
</script>

<svelte:window bind:innerWidth={width} />

{#if items.length > 0}
	<div {id}></div>
	<Card
		--card-content-padding="0"
		--card-title-padding="0 0 16px 0"
		--card-background-color="transparent"
		{open}
		onclick={() => (open = !open)}
	>
		{#snippet title()}
			{#if _title}
				{@render _title()}
			{/if}
		{/snippet}

		<div class="grid">
			{#each items.slice(0, width < 940 ? 6 : 8) as item (item.key)}
				<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<Item {item}></Item>
				</div>
			{/each}
		</div>
	</Card>
{/if}

<style>
	.grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;
	}

	@media screen and (min-width: 580px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 940px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
