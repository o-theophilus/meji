<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { app } from '$lib/store.svelte.js';
	import { Card } from '$lib/layout';
	import Item from './item.svelte';

	let { ops = $bindable() } = $props();

	let name = 'Items';
</script>

<Card
	open={ops.status == name}
	onclick={() => {
		ops.status = ops.status != name ? name : null;
	}}
>
	{#snippet title()}
		<div class="line space">
			<div class="title">{name}</div>
			{#if ops.status != name}
				<div class="c">
					<div class="a">Total Amount</div>
					<div class="b" transition:slide>
						₦{ops.total_items().toLocaleString()}
					</div>
				</div>
			{/if}
		</div>
	{/snippet}

	{#each app.cart_items as item (item.key + JSON.stringify(item.variation))}
		<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
			<Item {item} />
		</div>
	{/each}

	<div class="line space total">
		<span class="a">Total Amount</span>
		<div class="b">
			₦{ops.total_items().toLocaleString()}
		</div>
	</div>
</Card>

<style>
	.title {
		font-size: 1.2rem;
	}

	.c {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}
	.a {
		font-size: 0.8rem;
	}
	.b {
		font-weight: bold;
		font-size: 1.2rem;
		color: var(--ft1);
	}
	.total {
		margin-top: 16px;
		padding-top: 16px;
		border-top: 1px solid var(--bg2);
	}
</style>
