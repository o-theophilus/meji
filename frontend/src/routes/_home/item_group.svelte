<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Card } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import One from '../shop/item.svelte';

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
			{#each items as item, i (item.key)}
				<div
					class="item"
					class:can_hide={i > 5}
					animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}
				>
					<One {item}></One>
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

	.item {
		&.can_hide {
			display: none;
		}

		@media screen and (min-width: 940px) {
			&.can_hide {
				display: block;
			}
		}
	}
</style>
